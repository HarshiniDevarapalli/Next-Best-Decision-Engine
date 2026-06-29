# backend/services/ai/incident_parser.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from typing import Any, Dict, List


class IncidentContext(BaseModel):
    summary: str

    crisis_type: str

    severity: str

    supplier_entities: List[Dict[str, Any]] = Field(default_factory=list)

    vendor_entities: List[Dict[str, Any]] = Field(default_factory=list)

    inventory_entities: List[Dict[str, Any]] = Field(default_factory=list)

    contract_entities: List[Dict[str, Any]] = Field(default_factory=list)

    logistics_entities: List[Dict[str, Any]] = Field(default_factory=list)

    affected_products: List[str] = Field(default_factory=list)

    affected_locations: List[str] = Field(default_factory=list)

    affected_business_units: List[str] = Field(default_factory=list)

    dependencies: List[str] = Field(default_factory=list)

    identified_risks: List[str] = Field(default_factory=list)

    weak_signals: List[str] = Field(default_factory=list)

    assumptions: List[str] = Field(default_factory=list)

    missing_information: List[str] = Field(default_factory=list)

    recommended_data_sources: List[str] = Field(default_factory=list)

    confidence: float


class IncidentParser:

    def __init__(self, api_key: str):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        ).with_structured_output(IncidentContext)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the Incident Intelligence Agent for an Enterprise
Supply Chain Crisis Decision Engine.

Your job is to understand the incident and prepare it for
other agents.

The organization has these enterprise knowledge sources:

- Supplier Contracts
- Vendors
- Inventory
- Enterprise Policies
- News
- Historical Incidents

Extract everything useful for those agents.

Identify:

• crisis_type
• summary
• severity
• suppliers
• vendors
• inventory
• contracts
• logistics
• affected products
• affected locations
• business units
• dependencies
• risks
• weak signals
• assumptions
• missing information

Finally recommend which datasource agents should be used.

Allowed datasource names:

SupplierContractAgent
VendorAgent
InventoryAgent
PolicyAgent
NewsAgent
IncidentHistoryAgent

Return structured output only.

Never invent facts.
Leave fields empty if unknown.
"""
                ),
                (
                    "human",
                    "{incident}"
                )
            ]
        )

        self.chain = self.prompt | self.llm

    def parse(self, incident: str) -> IncidentContext:

        return self.chain.invoke(
            {
                "incident": incident
            }
        )