# backend/services/ai/risk_chain.py

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import RISK_PROMPT
from backend.services.aioutput_parsers import RiskAssessment


class RiskChain:
    """
    Enterprise Supply Chain Risk Intelligence

    Consumes:
    - Parsed Incident
    - Supplier Contracts
    - Vendors
    - Inventory
    - Policies
    - News
    - Incident History
    - Weak Signal Analysis

    Produces a unified enterprise risk assessment.
    """

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(RiskAssessment)

        self.chain = RISK_PROMPT | self.llm

    def invoke(
        self,
        *,
        parsed_incident: dict,
        datasource_context: dict,
        weak_signal_analysis: dict,
        planner_context: dict,
    ) -> RiskAssessment:

        context = {
            "planner": planner_context,
            "incident": parsed_incident,
            "enterprise_knowledge": datasource_context,
            "weak_signal_analysis": weak_signal_analysis,
        }

        return self.chain.invoke(
            {
                "context": context,
            }
        )