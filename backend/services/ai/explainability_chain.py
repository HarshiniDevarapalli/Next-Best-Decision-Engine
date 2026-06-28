# backend/services/ai/explainability_chain.py

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import EXPLAINABILITY_PROMPT
from backend.services.aioutput_parsers import ExplainabilityReport


class ExplainabilityChain:
    """
    Enterprise Explainability Agent

    Produces an executive explanation by combining:

    - Planner decisions
    - Parsed incident
    - Enterprise datasource evidence
    - Weak signal analysis
    - Risk assessment
    - Recommendations

    """

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(ExplainabilityReport)

        self.chain = EXPLAINABILITY_PROMPT | self.llm

    # backend/services/ai/explainability_chain.py
# (Update invoke() only)

def invoke(
    self,
    *,
    parsed_incident: dict,
    datasource_context: dict,
    weak_signal_analysis: dict,
    risk_report: dict,
    recommendation_report: dict,
    simulation_report: dict,
    decision_scores: dict,
    cost_report: dict,
    timeline_report: dict,
    scenario_comparison: dict,
    planner_context: dict,
):

    context = {
        "planner": planner_context,
        "incident": parsed_incident,
        "enterprise_context": datasource_context,
        "weak_signal": weak_signal_analysis,
        "risk": risk_report,
        "recommendation": recommendation_report,
        "simulation": simulation_report,
        "decision_scores": decision_scores,
        "cost_analysis": cost_report,
        "timeline_prediction": timeline_report,
        "scenario_comparison": scenario_comparison,
    }

    return self.chain.invoke(
        {
            "context": context
        }
    )