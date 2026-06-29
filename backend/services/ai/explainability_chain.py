from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.services.ai.output_parsers import ExplainabilityReport


EXPLAINABILITY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an Enterprise Explainability Agent.

Generate a clear executive explanation covering:

- incident summary
- evidence used
- weak signals
- risk assessment
- recommendations
- why the recommendations were chosen
- confidence

Return structured output only.
""",
        ),
        (
            "human",
            "{context}",
        ),
    ]
)


class ExplainabilityChain:
    """
    Enterprise Explainability Agent.
    """

    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(ExplainabilityReport)

        self.chain = EXPLAINABILITY_PROMPT | self.llm

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
                "context": context,
            }
        )