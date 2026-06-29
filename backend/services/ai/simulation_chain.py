# backend/services/ai/simulation_chain.py

from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class Scenario(BaseModel):
    title: str
    description: str
    probability: float
    business_impact: str
    operational_impact: str
    recommended_action: str


class SimulationReport(BaseModel):
    baseline: str
    scenarios: List[Scenario] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    best_scenario: str
    worst_scenario: str
    confidence: float


class SimulationChain:

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(SimulationReport)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an Enterprise What-If Simulation Agent.

Generate multiple realistic future scenarios.

For each scenario provide:

- title
- description
- probability
- operational impact
- business impact
- recommended action

Return structured output only.
"""
                ),
                (
                    "human",
                    "{context}"
                )
            ]
        )

        self.chain = self.prompt | self.llm

    def invoke(
        self,
        *,
        incident: dict,
        datasource_context: dict,
        risk_report: dict,
        recommendation_report: dict,
    ):

        context = {
            "incident": incident,
            "enterprise_context": datasource_context,
            "risk": risk_report,
            "recommendations": recommendation_report,
        }

        return self.chain.invoke(
            {
                "context": context
            }
        )