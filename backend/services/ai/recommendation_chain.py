# backend/services/ai/recommendation_chain.py

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import RECOMMENDATION_PROMPT
from backend.services.aioutput_parsers import RecommendationReport


class RecommendationChain:
    """
    Enterprise Supply Chain Decision Agent

    Uses:
    - Planner decisions
    - Parsed incident
    - Enterprise datasource evidence
    - Weak signals
    - Risk assessment

    Produces executable recommendations.
    """

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(RecommendationReport)

        self.chain = RECOMMENDATION_PROMPT | self.llm

    def invoke(
        self,
        *,
        parsed_incident: dict,
        datasource_context: dict,
        weak_signal_analysis: dict,
        risk_report: dict,
        planner_context: dict,
    ) -> RecommendationReport:

        context = {
            "planner": planner_context,
            "incident": parsed_incident,
            "enterprise_knowledge": datasource_context,
            "weak_signal_analysis": weak_signal_analysis,
            "risk_assessment": risk_report,
        }

        return self.chain.invoke(
            {
                "context": context
            }
        )