# backend/rag/test_rag.py

from backend.rag.rag_service import EnterpriseRAGService

rag = EnterpriseRAGService()

results = rag.search(
    "supplier delay in Germany",
    k=3,
)

for i, r in enumerate(results, 1):
    print(f"\nResult {i}")
    print(r["metadata"])
    print(r["content"][:300])