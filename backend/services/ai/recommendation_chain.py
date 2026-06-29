from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.services.ai.output_parsers import RecommendationReport


RECOMMENDATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an Enterprise Supply Chain Decision Agent.

Using the incident, enterprise context, weak signal analysis and risk assessment,
generate practical, prioritized recommendations.

For every recommendation include:
- title
- description
- priority
- expected business benefit
- implementation effort
- dependencies
- rationale

Return structured output only.
""",
        ),
        (
            "human",
            "{context}",
        ),
    ]
)


class RecommendationChain:
    """
    Enterprise Supply Chain Decision Agent.
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
                "context": context,
            }
        )