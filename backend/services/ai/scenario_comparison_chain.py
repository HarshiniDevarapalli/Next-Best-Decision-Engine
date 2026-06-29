from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.services.ai.output_parsers import ScenarioComparisonReport


class ScenarioComparisonChain:
    """
    Compares simulated business scenarios and recommends the strongest one.
    """

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(ScenarioComparisonReport)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an Enterprise Scenario Comparison Engine.

Compare all available scenarios.

Evaluate:

- advantages
- disadvantages
- overall score

Recommend the strongest scenario.

Return ONLY the structured output.
"""
                ),
                (
                    "human",
                    """
Simulation Report

{simulation_report}

Decision Scores

{decision_scores}

Cost Analysis

{cost_report}

Timeline Prediction

{timeline_report}
"""
                ),
            ]
        )

        self.chain = self.prompt | self.llm

    def invoke(
        self,
        *,
        simulation_report: dict,
        decision_scores: dict,
        cost_report: dict,
        timeline_report: dict,
    ) -> ScenarioComparisonReport:

        return self.chain.invoke(
            {
                "simulation_report": simulation_report,
                "decision_scores": decision_scores,
                "cost_report": cost_report,
                "timeline_report": timeline_report,
            }
        )