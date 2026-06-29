"""
base_recommender.py

Abstract interface for all AI recommendation engines.

The platform should never know whether recommendations are
generated using:
- Gemini
- Claude
- GPT
- Rule Engine
- Future ML Models

It only communicates through this interface.
"""

from abc import ABC, abstractmethod

from models.risk_report import RiskReport
from services.weak_signal.schemas import WeakSignalReport

from .schemas import RecommendationReport


class RecommendationEngine(ABC):

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """
        Human readable engine name.
        """
        pass

    @property
    @abstractmethod
    def model_version(self) -> str:
        """
        Version of underlying model.
        """
        pass

    @abstractmethod
    def recommend(
        self,
        weak_signal_report: WeakSignalReport,
        risk_report: RiskReport
    ) -> RecommendationReport:
        """
        Generate an AI recommendation.

        Returns
        -------
        RecommendationReport
        """
        pass