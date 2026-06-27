"""
llm_detector.py

LLM-backed Weak Signal detector.

Current Provider:
    - Gemini

Future Providers:
    - Groq
    - OpenAI
    - Claude
    - DistilBERT

The rest of the platform should NEVER know
which provider is being used.
"""

import json
import os
import time

from dotenv import load_dotenv

from .base_detector import WeakSignalDetector
from .prompt import SYSTEM_PROMPT, build_prompt
from .parser import WeakSignalParser

from .schemas import WeakSignalReport

load_dotenv()


class LLMWeakSignalDetector(WeakSignalDetector):

    def __init__(self):

        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()

        self.model = os.getenv(
            "LLM_MODEL",
            "gemini-2.5-flash"
        )

        if self.provider == "gemini":

            from google import genai

            self.client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )

        elif self.provider == "groq":

            from groq import Groq

            self.client = Groq(
                api_key=os.getenv("GROQ_API_KEY")
            )

        else:

            raise ValueError(
                f"Unsupported provider: {self.provider}"
            )

    @property
    def detector_name(self):

        return f"{self.provider.upper()} Weak Signal Detector"

    @property
    def model_version(self):

        return self.model

    def predict(
        self,
        transcript: str
    ) -> WeakSignalReport:

        start = time.perf_counter()

        prompt = build_prompt(transcript)

        if self.provider == "gemini":

            response = self.client.models.generate_content(

                model=self.model,

                contents=[
                    SYSTEM_PROMPT,
                    prompt
                ]

            )

            raw_output = response.text

        elif self.provider == "groq":

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[

                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=0.2

            )

            raw_output = response.choices[0].message.content

        else:

            raise RuntimeError(
                "Provider not initialized."
            )

        processing_time = (
            time.perf_counter() - start
        ) * 1000

        return WeakSignalParser.parse(

            response=raw_output,

            detector_name=self.detector_name,

            model_version=self.model_version,

            processing_time_ms=processing_time

        )