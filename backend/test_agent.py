from backend.agents.reasoning.weak_signal_agent import WeakSignalAgent
from backend.agents.reasoning.risk_agent import RiskAssessmentAgent

from backend.models.execution_context import ExecutionContext

context = ExecutionContext(
    workflow_name="enterprise_crisis",
    case_id="CASE001"
)

context.context_data["meeting_transcript"] = """
On July 15, our primary semiconductor supplier unexpectedly
ceased operations following a factory fire.

Current inventory can sustain production
for only 8 days.

No alternate supplier has been activated.

Legal team is reviewing contractual obligations.

External news reports indicate significant disruption
across the supplier's region.
"""

# ------------------------
# Weak Signal Intelligence
# ------------------------

weak_agent = WeakSignalAgent()

weak_result = weak_agent.execute(context)

print("\n========== WEAK SIGNAL ==========\n")

print(weak_result)

print()

print(
    context.context_data["weak_signal_report"].model_dump_json(indent=4)
)

# ------------------------
# Risk Assessment
# ------------------------

risk_agent = RiskAssessmentAgent()

risk_result = risk_agent.execute(context)

print("\n========== RISK ==========\n")

print(risk_result)

print()

print(
    context.context_data["risk_report"].model_dump_json(indent=4)
)