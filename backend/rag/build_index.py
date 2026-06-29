# backend/rag/build_index.py
from backend.rag.indexer import EnterpriseIndexer


if __name__ == "__main__":

    indexer = EnterpriseIndexer(
        data_dir="backend/data"
    )

    stats = indexer.build_index()

    print("=" * 50)
    print("Enterprise Knowledge Base Built")
    print("=" * 50)
    print(stats)