"""
base_detector.py

Defines the abstract interface for all Weak Signal detectors.

The platform should never know whether signals are generated using:
- OpenAI
- Claude
- Gemini
- DistilBERT
- DeBERTa
- Any future model

All implementations must inherit from WeakSignalDetector.
"""

from abc import ABC, abstractmethod

from .schemas import WeakSignalReport


class WeakSignalDetector(ABC):
    """
    Abstract base class for all Weak Signal detection engines.

    Every implementation should analyze a meeting transcript
    and return a standardized WeakSignalReport.
    """

    @property
    @abstractmethod
    def detector_name(self) -> str:
        """
        Human-readable detector name.

        Example:
            "OpenAI GPT-4o Detector"
            "DistilBERT Detector"
        """
        pass

    @property
    @abstractmethod
    def model_version(self) -> str:
        """
        Version of the underlying model.

        Example:
            "gpt-4.1"
            "distilbert-v1"
        """
        pass

    @abstractmethod
    def predict(self, transcript: str) -> WeakSignalReport:
        """
        Analyze a meeting transcript and extract
        weak business signals.

        Parameters
        ----------
        transcript : str
            Raw meeting transcript.

        Returns
        -------
        WeakSignalReport
        """
        pass