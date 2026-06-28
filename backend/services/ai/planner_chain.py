# backend/services/ai/planner_chain.py

from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class ExecutionPlan(BaseModel):
    workflow: str

    objective: str

    crisis_type: str

    execution_strategy: str

    datasource_agents: List[str] = Field(default_factory=list)

    reasoning_agents: List[str] = Field(default_factory=list)

    execution_order: List[str] = Field(default_factory=list)

    parallel_groups: List[List[str]] = Field(default_factory=list)

    shadow_mode: bool

    what_if: bool

    requires_human_review: bool

    planner_reasoning: str

    confidence: float


class PlannerChain:

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(ExecutionPlan)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the MASTER PLANNER of an Enterprise Supply Chain Crisis
Decision Engine.

You NEVER solve the incident.

You ONLY produce an execution plan.

The platform contains these enterprise datasource agents:

1. SupplierContractAgent
   - Contracts
   - SLAs
   - Obligations
   - Dependencies

2. VendorAgent
   - Vendor status
   - Alternate vendors
   - Vendor capability
   - Vendor availability

3. InventoryAgent
   - Inventory
   - Safety stock
   - Stock coverage
   - Material availability

4. PolicyAgent
   - Internal policies
   - Compliance
   - Business continuity
   - SOPs

5. NewsAgent
   - External events
   - Weather
   - Geopolitics
   - Natural disasters
   - Supplier news

6. IncidentHistoryAgent
   - Similar historical incidents
   - Lessons learned
   - Previous resolutions

Reasoning agents:

- WeakSignalAgent
- RiskAgent
- RecommendationAgent
- ExplainabilityAgent

Your responsibilities:

1. Understand the incident.
2. Identify the crisis type.
3. Decide which datasource agents are required.
4. Decide reasoning order.
5. Decide execution strategy.
6. Decide parallel execution.
7. Enable Shadow Mode whenever beneficial.
8. Decide if human review is needed.
9. Never invoke unnecessary agents.

Only choose agents that provide useful information.

Return structured output only.
"""
                ),
                (
                    "human",
                    """
Workflow:
{workflow}

Mode:
{mode}

Incident:
{incident}
"""
                ),
            ]
        )

        self.chain = self.prompt | self.llm

    def plan(
        self,
        workflow: str,
        mode: str,
        incident: str,
    ) -> ExecutionPlan:

        return self.chain.invoke(
            {
                "workflow": workflow,
                "mode": mode,
                "incident": incident,
            }
        )
# backend/services/ai/planner_chain.py
# (Update planner prompt)

# Add this inside the planner system prompt:

"""
When appropriate, enable advanced decision intelligence.

Set:

simulation_enabled
decision_scoring_enabled
cost_analysis_enabled
timeline_prediction_enabled
scenario_comparison_enabled

Enable them for:

- Supply chain disruption
- Logistics delay
- Vendor failure
- Inventory shortage
- Manufacturing disruption
- Contract breach
- Business continuity incidents

Disable only for trivial informational workflows.
"""