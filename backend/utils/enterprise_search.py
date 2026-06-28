from backend.rag.hybrid_retriever import HybridRetriever


class EnterpriseSearch:

    SOURCE_MAP = {
        "vendors": "vendors.json",
        "inventory": "inventory.json",
        "supplier_contracts": "supplier_contracts.json",
        "policies": "policies.json",
        "news": "news.json",
        "incident_history": "incident_history.json",
    }

    def __init__(self):

        self.retriever = HybridRetriever()

    def search(
        self,
        datasource: str,
        parsed_incident: dict,
        k: int = 5,
    ):

        query = " ".join([
            parsed_incident.get("summary", ""),
            parsed_incident.get("crisis_type", ""),
            " ".join(parsed_incident.get("affected_products", [])),
            " ".join(parsed_incident.get("affected_locations", [])),
            " ".join(parsed_incident.get("identified_risks", [])),
        ])

        return self.retriever.retrieve(
            datasource=self.SOURCE_MAP[datasource],
            query=query,
            k=k,
        )