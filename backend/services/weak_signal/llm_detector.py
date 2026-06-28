# backend/services/weak_signal/llm_detector.py

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from backend.services.ai.output_parsers import ShadowComparison


class LLMWeakSignalDetector:

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

Analyze the incident together with the enterprise context.

Detect weak signals that could become future enterprise risks.

Return JSON only.

Output format:

{
    "signals":[
        {
            "title":"",
            "description":"",
            "severity":"",
            "confidence":0.0,
            "source":"",
            "category":""
        }
    ]
}

Do not recommend actions.
Do not calculate risk.
Do not explain.
Only detect weak signals.
"""
                ),
                (
                    "human",
                    """
Incident

{incident}

Enterprise Context

{context}
"""
                ),
            ]
        )

        self.chain = self.prompt | self.llm

    def detect(
        self,
        incident: str,
        parsed_incident: dict,
        context: dict,
    ):

        response = self.chain.invoke(
            {
                "incident": incident,
                "context": {
                    "parsed_incident": parsed_incident,
                    "enterprise_context": context,
                },
            }
        )

        return response.content