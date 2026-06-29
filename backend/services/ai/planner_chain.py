
# backend/services/ai/planner_chain.py

from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class ExecutionPlan(BaseModel):
    workflow: str
    objective: str
    crisis_type: str
    execution_strategy: str

    datasource_agents: List[str] = Field(default_factory=list)
    reasoning_agents: List[str] = Field(default_factory=list)

    execution_order: List[str] = Field(default_factory=list)
    parallel_groups: List[List[str]] = Field(default_factory=list)

    shadow_mode: bool
    what_if: bool
    requires_human_review: bool

    planner_reasoning: str
    confidence: float


class PlannerChain:

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(ExecutionPlan)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
        You are the Enterprise Workflow Planner for an AI-driven supply chain decision platform.

        Your responsibility is to create an execution plan for every incident.

        ===========================================================
        AVAILABLE DATASOURCE AGENTS
        ===========================================================

        - SupplierContractAgent
        Retrieves supplier contracts, SLAs, obligations and penalties.

        - VendorAgent
        Retrieves approved vendors, supplier capacity and lead times.

        - InventoryAgent
        Retrieves inventory levels, warehouse information and shortages.

        - PolicyAgent
        Retrieves internal procurement and business continuity policies.

        - NewsAgent
        Retrieves external intelligence and current events.

        - IncidentHistoryAgent
        Retrieves historical incidents and previous resolutions.

        ===========================================================
        AVAILABLE REASONING AGENTS
        ===========================================================

        - WeakSignalAgent
        Parses the incident and detects weak signals.

        - RiskAgent
        Performs enterprise risk assessment.

        - RecommendationAgent
        Generates mitigation recommendations.

        - WhatIfAgent
        Simulates alternative future scenarios.

        - DecisionScoringAgent
        Scores and ranks candidate actions.

        - CostImpactAgent
        Estimates financial and operational impact.

        - TimelinePredictionAgent
        Predicts recovery timeline and milestones.

        - ScenarioComparisonAgent
        Compares simulated scenarios and recommends the best option.

        - ExplainabilityAgent
        Produces the final explanation and reasoning summary.
        This agent must always execute last.

        ===========================================================
        PLANNING RULES
        ===========================================================

        Datasource Agents
        -----------------
        Select ONLY the datasource agents required for the incident.

        Reasoning Agents
        ----------------

        WeakSignalAgent
        - Use whenever the incident requires parsing or weak signal detection.

        RiskAgent
        - Required for operational decision-making.

        RecommendationAgent
        - Execute after RiskAgent.

        WhatIfAgent
        Use when:
        - incident severity is High or Critical
        - uncertainty exists
        - multiple response strategies are possible
        - business continuity is affected

        DecisionScoringAgent
        Use when:
        - recommendations need prioritization
        - multiple actions are available
        - WhatIfAgent is selected

        CostImpactAgent
        Use when:
        - procurement decisions exist
        - inventory decisions exist
        - logistics decisions exist
        - production is affected
        - financial trade-offs are involved

        TimelinePredictionAgent
        Use when:
        - recovery time matters
        - production may stop
        - logistics delays exist
        - supplier disruptions exist

        ScenarioComparisonAgent
        Use when:
        - multiple simulated scenarios exist
        - WhatIfAgent has been selected

        ExplainabilityAgent
        - Always execute last.

        ===========================================================
        EXECUTION RULES
        ===========================================================

        1. Datasource agents may execute in parallel.
        2. Reasoning agents execute sequentially.
        3. execution_order must contain every selected agent.
        4. parallel_groups should contain only datasource agents.
        5. Return ONLY valid structured output matching ExecutionPlan.
        6. Do not invent agent names.

        The planner should choose the minimum number of agents necessary while ensuring complete decision support.
        """
                ),
                (
                    "human",
                    """
        Workflow:
        {workflow}

        Mode:
        {mode}

        Incident:
        {incident}
        """
                ),
            ]
        )
        self.chain = self.prompt | self.llm

    def plan(
    self,
    workflow: str,
    mode: str,
    incident: str,
    ) -> ExecutionPlan:

        return self.chain.invoke(
            {
                "workflow": workflow,
                "mode": mode,
                "incident": incident,
            }
        )