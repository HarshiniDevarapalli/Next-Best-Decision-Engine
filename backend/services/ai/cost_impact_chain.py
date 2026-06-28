# backend/services/ai/cost_impact_chain.py

from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class CostImpact(BaseModel):
    action: str
    estimated_cost: str
    operational_impact: str
    financial_impact: str
    roi: str


class CostImpactReport(BaseModel):
    impacts: List[CostImpact] = Field(default_factory=list)
    lowest_cost_option: str
    highest_roi_option: str
    confidence: float


class CostImpactChain:

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(CostImpactReport)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the Enterprise Cost Impact Agent.

Estimate:

- implementation cost
- financial impact
- operational impact
- ROI

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
        recommendation_report: dict,
        simulation_report: dict,
    ):

        return self.chain.invoke(
            {
                "context": {
                    "incident": incident,
                    "recommendations": recommendation_report,
                    "simulation": simulation_report,
                }
            }
        )