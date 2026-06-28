from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    """
    Local embedding model for enterprise RAG.

    Advantages:
    - No API cost
    - No rate limits
    - Fast
    - Offline
    """

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

    def get(self):
        return self.embeddings