# backend/rag/indexer.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.rag.document_loader import EnterpriseDocumentLoader
from backend.rag.vector_store import EnterpriseVectorStore


class EnterpriseIndexer:
    """
    Creates and updates the enterprise vector database.

    Pipeline:
    Documents
        ↓
    Chunking
        ↓
    Embeddings
        ↓
    Chroma Vector Store
    """

    def __init__(self, data_dir: str):

        self.loader = EnterpriseDocumentLoader(data_dir)

        self.vector_store = EnterpriseVectorStore().get()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def build_index(self):

        documents = self.loader.load()

        chunks = self.splitter.split_documents(documents)

        if chunks:
            self.vector_store.add_documents(chunks)

        return {
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
        }

    def update_index(self):

        return self.build_index()