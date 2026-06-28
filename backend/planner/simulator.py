"""
simulator.py

What-If Simulator orchestration logic.

This module does NOT modify the existing Planner, agents, or
registry. It reuses them as-is, calling agents directly in a
custom sequence so we can inject overrides between the
datasource phase and the reasoning phase.

Why not just reuse Planner.execute_workflow()?
-----------------------------------------------
Planner.execute_workflow() runs the full workflow in one pass
with no place to inject overrides partway through. Rather than
changing that shared, working code (and risking breaking the
normal /workflow/run endpoint for the rest of the team), this
module re-implements the same two-phase sequence (datasource
agents, then reasoning agents) with one extra step in between:
applying overrides to context_data.

DATASOURCE_AGENT_NAMES and REASONING_AGENT_NAMES mirror the
order defined in data/workflows/crisis_response.json. If that
workflow file changes, this list should be updated to match.
"""

from typing import Any, Dict

from models.execution_context import ExecutionContext
from registry.registry import AgentRegistry


DATASOURCE_AGENT_NAMES = [
    "supplier_contract",
    "inventory",
    "vendor",
    "policy",
    "news",
    "incident_history",
]

REASONING_AGENT_NAMES = [
    "weak_signal",
    "risk",
    "recommendation",
    "explainability",
]


def _run_agents(
    agent_names: list[str],
    context: ExecutionContext,
    registry: AgentRegistry,
) -> None:
    """
    Run a list of agents, in order, against a shared context.
    Mirrors what Planner.execute_workflow() does internally.
    """

    for agent_name in agent_names:

        if not registry.is_registered(agent_name):
            continue

        agent = registry.get(agent_name)
        result = agent.execute(context)

        context.agent_results.append(result)
        context.context_data[agent_name] = result.data


def _apply_overrides(
    context: ExecutionContext,
    overrides: Dict[str, Any],
) -> None:
    """
    Apply field-level overrides on top of real datasource data,
    directly inside context.context_data.

    Two override shapes are supported:

    1. Dict-shaped agents (e.g. "inventory", "supplier_contract",
       "news") - the override dict is shallow-merged into the
       existing record, so callers only need to specify the
       fields they want to change.

    2. List-shaped agents with a special "_set_all" key (used
       for "vendor", whose real data is {"vendors": [...]})
       - {"vendor": {"_set_all": {"approved_vendor": false}}}
       applies that field/value to every item in the list, e.g.
       to simulate "no backup vendor is available" without the
       caller needing to know individual vendor names.
    """

    for agent_name, fields in overrides.items():

        existing = context.context_data.get(agent_name, {})

        if not isinstance(existing, dict):
            continue

        if "_set_all" in fields:

            set_all_fields = fields["_set_all"]
            updated = dict(existing)

            for key, value in updated.items():

                if isinstance(value, list):

                    updated[key] = [
                        {**item, **set_all_fields}
                        if isinstance(item, dict)
                        else item
                        for item in value
                    ]

            context.context_data[agent_name] = updated

        else:

            merged = {**existing, **fields}
            context.context_data[agent_name] = merged


def run_simulation(
    workflow_name: str,
    case_id: str,
    overrides: Dict[str, Any],
    registry: AgentRegistry,
) -> ExecutionContext:
    """
    Run the full crisis_response pipeline twice on the same
    base case data:

    1. BASELINE  - the real, unmodified case data
    2. SIMULATED - the same case data, with overrides applied
                   before the reasoning agents run

    Returns a single ExecutionContext whose context_data
    contains both "baseline" and "simulated" keys, each holding
    a full set of reasoning outputs, so the frontend can show
    a side-by-side comparison.
    """

    base_context = ExecutionContext(
        workflow_name=workflow_name,
        case_id=case_id,
    )
    _run_agents(DATASOURCE_AGENT_NAMES, base_context, registry)

    baseline_context = ExecutionContext(
        workflow_name=workflow_name,
        case_id=case_id,
    )
    baseline_context.context_data = {
        key: value for key, value in base_context.context_data.items()
    }
    _run_agents(REASONING_AGENT_NAMES, baseline_context, registry)

    simulated_context = ExecutionContext(
        workflow_name=workflow_name,
        case_id=case_id,
    )
    simulated_context.context_data = {
        key: value for key, value in base_context.context_data.items()
    }
    _apply_overrides(simulated_context, overrides)
    _run_agents(REASONING_AGENT_NAMES, simulated_context, registry)

    result_context = ExecutionContext(
        workflow_name=workflow_name,
        case_id=case_id,
    )
    result_context.status = "SUCCESS"
    result_context.context_data = {
        "baseline": baseline_context.context_data,
        "simulated": simulated_context.context_data,
        "overrides_applied": overrides,
    }

    return result_context