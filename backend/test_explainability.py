from agents.reasoning.weak_signal_agent import WeakSignalAgent
from agents.reasoning.risk_agent import RiskAssessmentAgent
from agents.reasoning.recommendation_agent import RecommendationAgent
from agents.reasoning.explainability_agent import ExplainabilityAgent

from models.execution_context import ExecutionContext

context = ExecutionContext(
    workflow_name="enterprise_crisis",
    case_id="CASE001"
)

context.context_data["meeting_transcript"] = """
On July 15, our primary semiconductor supplier unexpectedly ceased operations following a factory fire.

Current inventory can sustain production for only 8 days.

No alternate supplier has been activated.

Legal team is reviewing contractual obligations.

External news reports indicate significant disruption across the supplier's region.
"""

WeakSignalAgent().execute(context)
RiskAssessmentAgent().execute(context)
RecommendationAgent().execute(context)
ExplainabilityAgent().execute(context)

print(
    context.context_data[
        "explainability_report"
    ].model_dump_json(indent=4)
)