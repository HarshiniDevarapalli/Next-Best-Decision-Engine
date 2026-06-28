# backend/agents/datasource/supplier_contract_agent.py

from typing import Any, Dict, List

from backend.agents.datasource.base_datasource_agent import BaseDatasourceAgent


class SupplierContractAgent(BaseDatasourceAgent):
    """
    Enterprise Supplier Contract Intelligence Agent
    """

    DATASOURCE = "supplier_contracts"

    def __init__(self):
        super().__init__("SupplierContractAgent")

    def analyze(
        self,
        records: List[Dict[str, Any]],
        parsed_incident: Dict[str, Any],
    ) -> Dict[str, Any]:

        matching_contracts = []
        obligations = []
        sla_breaches = []
        force_majeure = []
        alternate_suppliers = []
        contractual_risks = []
        insights = []

        for record in records:

            matching_contracts.append(record)

            obligations.extend(
                record.get("obligations", [])
            )

            if record.get("sla_status") == "BREACHED":
                sla_breaches.append(record)

            if record.get("force_majeure"):
                force_majeure.append(record)

            if record.get("alternate_supplier"):
                alternate_suppliers.append(
                    record["alternate_supplier"]
                )

            if record.get("risk"):
                contractual_risks.append(record["risk"])

        if sla_breaches:
            insights.append(
                f"{len(sla_breaches)} SLA breaches detected."
            )

        if force_majeure:
            insights.append(
                "Force majeure clauses identified."
            )

        return {
            "matching_contracts": matching_contracts,
            "obligations": obligations,
            "sla_breaches": sla_breaches,
            "force_majeure_clauses": force_majeure,
            "alternate_suppliers": alternate_suppliers,
            "identified_risks": contractual_risks,
            "insights": insights,
        }