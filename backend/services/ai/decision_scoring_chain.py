from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.services.ai.output_parsers import DecisionScoringReport


class DecisionScoringChain:
    """
    Scores and ranks candidate enterprise decisions.
    """

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(DecisionScoringReport)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an Enterprise Decision Scoring Engine.

Evaluate each recommendation using:

- feasibility
- business value
- operational risk
- implementation effort
- overall score

Return ONLY the structured output.
"""
                ),
                (
                    "human",
                    """
Incident

{incident}

Risk Assessment

{risk_report}

Recommendation Report

{recommendation_report}

Simulation Report

{simulation_report}
"""
                ),
            ]
        )

        self.chain = self.prompt | self.llm

    def invoke(
        self,
        *,
        incident: dict,
        risk_report: dict,
        recommendation_report: dict,
        simulation_report: dict,
    ) -> DecisionScoringReport:

        return self.chain.invoke(
            {
                "incident": incident,
                "risk_report": risk_report,
                "recommendation_report": recommendation_report,
                "simulation_report": simulation_report,
            }
        )