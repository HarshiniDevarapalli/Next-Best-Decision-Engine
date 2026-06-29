# backend/rag/retriever.py

from typing import List

from langchain_core.documents import Document

from backend.rag.vector_store import EnterpriseVectorStore


class EnterpriseRetriever:
    """
    Semantic retriever for enterprise knowledge.

    Used by:
    - VendorAgent
    - InventoryAgent
    - SupplierContractAgent
    - PolicyAgent
    - NewsAgent
    - IncidentHistoryAgent
    """

    def __init__(self):

        self.db = EnterpriseVectorStore().get()

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> List[Document]:

        return self.db.similarity_search(
            query=query,
            k=k,
        )

    def retrieve_with_scores(
        self,
        query: str,
        k: int = 5,
    ):

        return self.db.similarity_search_with_score(
            query=query,
            k=k,
        )