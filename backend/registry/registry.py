# backend/registry/registry.py
# (Final integration update for Planner-driven architecture)

import os

from backend.agents.datasource.supplier_contract_agent import SupplierContractAgent
from backend.agents.datasource.vendor_agent import VendorAgent
from backend.agents.datasource.inventory_agent import InventoryAgent
from backend.agents.datasource.policy_agent import PolicyAgent
from backend.agents.datasource.news_agent import NewsAgent
from backend.agents.datasource.incident_history_agent import IncidentHistoryAgent

from backend.agents.reasoning.weak_signal_agent import WeakSignalAgent
from backend.agents.reasoning.risk_agent import RiskAgent
from backend.agents.reasoning.recommendation_agent import RecommendationAgent
from backend.agents.reasoning.explainability_agent import ExplainabilityAgent

from backend.servicesweak_signal.rule_detector import RuleBasedDetector


class AgentRegistry:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        self.datasource_agents = {
            "SupplierContractAgent": SupplierContractAgent(),
            "VendorAgent": VendorAgent(),
            "InventoryAgent": InventoryAgent(),
            "PolicyAgent": PolicyAgent(),
            "NewsAgent": NewsAgent(),
            "IncidentHistoryAgent": IncidentHistoryAgent(),
        }

        self.reasoning_agents = {
            "WeakSignalAgent": WeakSignalAgent(
                rule_detector=RuleBasedDetector(),
                api_key=api_key,
            ),
            "RiskAgent": RiskAgent(api_key),
            "RecommendationAgent": RecommendationAgent(api_key),
            "ExplainabilityAgent": ExplainabilityAgent(api_key),
        }

    def get_datasource_agent(self, agent_name: str):
        return self.datasource_agents.get(agent_name)

    def get_reasoning_agent(self, agent_name: str):
        return self.reasoning_agents.get(agent_name)

    def get_all_datasource_agents(self):
        return self.datasource_agents

    def get_all_reasoning_agents(self):
        return self.reasoning_agents


# Global registry used by LangGraph
registry = AgentRegistry()

# backend/registry/registry.py
# (Add Phase 4 reasoning agents)

from backend.agents.reasoning.what_if_agent import WhatIfAgent
from backend.agents.reasoning.decision_scoring_agent import DecisionScoringAgent
from backend.agents.reasoning.cost_impact_agent import CostImpactAgent
from backend.agents.reasoning.timeline_prediction_agent import TimelinePredictionAgent
from backend.agents.reasoning.scenario_comparison_agent import ScenarioComparisonAgent


# Add inside self.reasoning_agents

self.reasoning_agents.update({

    "WhatIfAgent": WhatIfAgent(api_key),

    "DecisionScoringAgent": DecisionScoringAgent(api_key),

    "CostImpactAgent": CostImpactAgent(api_key),

    "TimelinePredictionAgent": TimelinePredictionAgent(api_key),

    "ScenarioComparisonAgent": ScenarioComparisonAgent(api_key),

})