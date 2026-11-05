import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from backend.retriever import retrieve_information

question = "ಡೆಂಗ್ಯೂ ಹೇಗೆ ಹರಡುತ್ತದೆ?"

results = retrieve_information(
    question=question,
    disease="Dengue",
    top_k=5
)

print("\nDENGUE TRANSMISSION RETRIEVAL TEST")
print("=" * 70)

for index, result in enumerate(results, start=1):
    print(f"\nRESULT {index}")
    print(f"Document: {result['document_name']}")
    print(f"Page: {result['page_number']}")
    print(f"Similarity: {result['similarity']}")
    print("\nRetrieved text:")
    print(result["text"])
    print("-" * 70)