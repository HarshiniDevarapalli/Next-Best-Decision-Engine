# backend/rag/hybrid_retriever.py

from typing import Dict, List

from backend.rag.rag_service import EnterpriseRAGService


class HybridRetriever:
    """
    Hybrid enterprise retrieval.

    Phase 3:
    - Semantic search (Chroma)

    Future:
    - BM25 keyword search
    - Reciprocal Rank Fusion (RRF)
    - Cross-encoder reranking
    """

    def __init__(self):

        self.rag = EnterpriseRAGService()

    def retrieve(
        self,
        datasource: str,
        query: str,
        k: int = 5,
    ) -> List[Dict]:

        results = self.rag.search(
            query=query,
            source=datasource,
            k=k,
        )

        return sorted(
            results,
            key=lambda x: len(x["content"]),
            reverse=True,
        )