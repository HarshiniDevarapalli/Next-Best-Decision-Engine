# backend/rag/vector_store.py

from pathlib import Path

from langchain_chroma import Chroma
from backend.rag.embeddings import EmbeddingService


class EnterpriseVectorStore:
    """
    Persistent vector database for enterprise knowledge.

    Stores:
    - Policies
    - Contracts
    - Incident Reports
    - Vendor Information
    - Inventory Documents
    - External Intelligence
    """

    def __init__(self):

        self.persist_directory = Path("backend/vector_db")

        self.embedding_function = (
            EmbeddingService().get()
        )

        self.db = Chroma(
            persist_directory=str(self.persist_directory),
            embedding_function=self.embedding_function,
            collection_name="enterprise_knowledge",
        )

    def get(self):

        return self.db