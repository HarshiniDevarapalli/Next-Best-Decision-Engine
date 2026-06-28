"""
gemini_client.py

Reusable Gemini client for the NBDE platform.

Any future agent can use this client instead of talking
to Gemini directly.
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "LLM_MODEL",
            "gemini-2.5-flash"
        )

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2
    ) -> str:
        """
        Generate structured JSON output.
        """

        response = self.client.models.generate_content(

            model=self.model,

            contents=[
                system_prompt,
                user_prompt
            ],

            config=types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json"
            )

        )

        return response.text