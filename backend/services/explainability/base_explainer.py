"""
base_explainer.py

Abstract interface for Explainability Engines.

The platform should never know whether explainability
is generated using:
- Gemini
- Claude
- GPT
- Rule Engine
- Future AI Models

All implementations must inherit from ExplainabilityEngine.
"""

from abc import ABC, abstractmethod

from services.weak_signal.schemas import WeakSignalReport
from models.risk_report import RiskReport
from services.recommendation.schemas import RecommendationReport

from .schemas import ExplainabilityReport


class ExplainabilityEngine(ABC):

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """
        Human-readable engine name.
        """
        pass

    @property
    @abstractmethod
    def model_version(self) -> str:
        """
        Underlying model version.
        """
        pass

    @abstractmethod
    def explain(
        self,
        weak_signal_report: WeakSignalReport,
        risk_report: RiskReport,
        recommendation_report: RecommendationReport
    ) -> ExplainabilityReport:
        """
        Generate an executive explainability report.
        """
        pass