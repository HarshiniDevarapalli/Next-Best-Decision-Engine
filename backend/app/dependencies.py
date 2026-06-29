# backend/app/dependencies.py

import os

from dotenv import load_dotenv

from backend.graph.workflow_graph import enterprise_workflow


load_dotenv()


def get_workflow():
    return enterprise_workflow


def get_gemini_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found.")

    return api_key