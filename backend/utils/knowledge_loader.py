# backend/utils/knowledge_loader.py

import json
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class EnterpriseKnowledgeLoader:
    """
    Central knowledge loader.

    Today:
        JSON files

    Future:
        RAG
        PostgreSQL
        SAP
        Oracle
        REST APIs
    """

    FILES = {
        "inventory": "inventory.json",
        "vendors": "vendors.json",
        "supplier_contracts": "supplier_contracts.json",
        "policies": "policies.json",
        "incident_history": "incident_history.json",
        "news": "news.json",
    }

    @classmethod
    def load(cls, source: str) -> List[Dict[str, Any]]:

        filename = cls.FILES.get(source)

        if filename is None:
            raise ValueError(f"Unknown datasource: {source}")

        path = DATA_DIR / filename

        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def search(
        cls,
        source: str,
        keywords: List[str],
    ) -> List[Dict[str, Any]]:

        records = cls.load(source)

        if not keywords:
            return records

        results = []

        keywords = [k.lower() for k in keywords]

        for record in records:

            text = json.dumps(record).lower()

            if any(keyword in text for keyword in keywords):
                results.append(record)

        return results