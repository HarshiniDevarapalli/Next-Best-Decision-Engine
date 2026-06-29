# backend/services/weak_signal/llm_detector.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


class LLMWeakSignalDetector:
    """
    LLM-based weak signal detector.

    Uses Gemini to identify emerging weak signals from an incident and
    enterprise context.
    """

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an Enterprise Weak Signal Detection Agent.

Your job is to identify early warning indicators from an enterprise incident.

Analyze:
- the incident
- parsed incident information
- enterprise context

Identify:
- weak signals
- emerging risks
- signal confidence
- signal category
- supporting evidence

Do NOT:
- recommend actions
- calculate business risk
- estimate financial impact
- explain recommendations

Respond ONLY with valid JSON.
""",
                ),
                (
                    "human",
                    """
Incident:
{incident}

Parsed Incident:
{parsed_incident}

Enterprise Context:
{enterprise_context}
""",
                ),
            ]
        )

        self.chain = self.prompt | self.llm

    def detect(
        self,
        *,
        incident: str,
        parsed_incident: dict,
        context: dict,
        planner_context: dict | None = None,
    ):

        response = self.chain.invoke(
            {
                "incident": incident,
                "parsed_incident": parsed_incident,
                "enterprise_context": context,
            }
        )

        # If Gemini returns plain text
        if hasattr(response, "content"):
            return response.content

        return response