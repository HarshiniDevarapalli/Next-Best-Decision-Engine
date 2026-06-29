from typing import Any, Dict, List, Optional

from backend.rag.vector_store import EnterpriseVectorStore


class EnterpriseRAGService:
    """
    Enterprise semantic search service.

    Supports:
    - Semantic search
    - Metadata filtering
    - Top-k retrieval
    """

    def __init__(self):

        self.db = EnterpriseVectorStore().get()

    def search(
        self,
        query: str,
        k: int = 5,
        source: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        if source:

            docs = self.db.similarity_search(
                query=query,
                k=k,
                filter={
                    "source": source,
                },
            )

        else:

            docs = self.db.similarity_search(
                query=query,
                k=k,
            )

        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in docs
        ]