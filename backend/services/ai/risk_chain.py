# backend/services/ai/risk_chain.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.services.ai.output_parsers import RiskAssessment


RISK_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an Enterprise Supply Chain Risk Intelligence Agent.

Analyze the supplied incident and enterprise context.

Assess:
- Overall risk level
- Business impact
- Operational impact
- Financial impact
- Regulatory impact
- Critical risks
- Risk justification

Return structured output only.
""",
        ),
        (
            "human",
            "{context}",
        ),
    ]
)


class RiskChain:
    """
    Enterprise Supply Chain Risk Intelligence
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