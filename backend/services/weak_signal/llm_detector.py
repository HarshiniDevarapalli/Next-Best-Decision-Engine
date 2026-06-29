"""
llm_detector.py

LLM-backed Weak Signal Detector.

The detector is responsible only for:
1. Building prompts
2. Calling the LLM client
3. Parsing the response

The actual LLM provider (Gemini today, Groq tomorrow)
is hidden behind GeminiClient.
"""


import time

from services.llm.gemini_client import GeminiClient

from .base_detector import WeakSignalDetector
from .prompt import SYSTEM_PROMPT, build_prompt
from .parser import WeakSignalParser
from .schemas import WeakSignalReport


class LLMWeakSignalDetector(WeakSignalDetector):

    def __init__(self):

        self.client = GeminiClient()

    @property
    def detector_name(self):

        return "Gemini Weak Signal Detector"

    @property
    def model_version(self):

        return self.client.model

    
    def predict(
        self,
        transcript: str
    ) -> WeakSignalReport:

        start = time.perf_counter()

        raw_response = self.client.generate_json(

            system_prompt=SYSTEM_PROMPT,

            user_prompt=build_prompt(transcript)

        )

        processing_time = (
            time.perf_counter() - start
        ) * 1000

        return WeakSignalParser.parse(

            response=raw_response,

            detector_name=self.detector_name,

            model_version=self.model_version,

            processing_time_ms=processing_time

        )