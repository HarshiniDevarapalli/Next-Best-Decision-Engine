# backend/utils/retrieval.py

from typing import Any, Dict, List

from backend.utils.knowledge_loader import EnterpriseKnowledgeLoader


class EnterpriseRetriever:
    """
    Shared retrieval layer for all datasource agents.

    Every datasource agent should call this instead of
    directly accessing JSON files.
    """

    @staticmethod
    def retrieve(
        datasource: str,
        parsed_incident: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        keywords = []

        for field in (
            "supplier_entities",
            "vendor_entities",
            "inventory_entities",
            "contract_entities",
            "affected_products",
            "affected_locations",
            "identified_risks",
        ):

            values = parsed_incident.get(field, [])

            if isinstance(values, list):
                for value in values:
                    if isinstance(value, dict):
                        keywords.extend(str(v) for v in value.values())
                    else:
                        keywords.append(str(value))

        crisis = parsed_incident.get("crisis_type")
        if crisis:
            keywords.append(crisis)

        keywords = list(
            {
                k.strip().lower()
                for k in keywords
                if str(k).strip()
            }
        )

        return EnterpriseKnowledgeLoader.search(
            datasource,
            keywords,
        )