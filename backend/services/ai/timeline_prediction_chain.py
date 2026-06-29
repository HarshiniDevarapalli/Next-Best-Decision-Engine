from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.services.ai.output_parsers import TimelinePredictionReport


class TimelinePredictionChain:
    """
    Predicts recovery timeline and critical milestones.
    """

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(TimelinePredictionReport)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an Enterprise Recovery Timeline Predictor.

Estimate:

- recovery duration
- critical path
- milestones
- blockers

Return ONLY the structured output.
"""
                ),
                (
                    "human",
                    """
Incident

{incident}

Risk Report

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
    ) -> TimelinePredictionReport:

        return self.chain.invoke(
            {
                "incident": incident,
                "risk_report": risk_report,
                "recommendation_report": recommendation_report,
                "simulation_report": simulation_report,
            }
        )