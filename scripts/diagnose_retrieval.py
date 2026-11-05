from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_DIR = Path(__file__).resolve().parent.parent

model = SentenceTransformer("intfloat/multilingual-e5-small")

client = chromadb.PersistentClient(
    path=str(PROJECT_DIR / "chroma_db")
)

collection = client.get_collection(
    name="public_health_knowledge"
)

tests = [
    (
        "డెంగ్యూ జ్వరం లక్షణాలు ఏమిటి?",
        "Dengue"
    ),
    (
        "What are the common symptoms of pulmonary tuberculosis?",
        "Tuberculosis"
    ),
    (
        "What are the main causes of hypertension?",
        "Hypertension"
    ),
]

for question, disease in tests:

    embedding = model.encode(
        ["query: " + question],
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=embedding.tolist(),
        n_results=5,
        where={"disease": disease}
    )

    print("\n" + "=" * 65)
    print("QUESTION:", question)
    print("DISEASE:", disease)
    print("=" * 65)

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]
        similarity = 1 - results["distances"][0][i]

        print(f"\nResult {i + 1}")
        print("Similarity:", round(similarity, 4))
        print("Document:", metadata["document_name"])
        print("Page:", metadata["page_number"])
        print("Text:", document[:700])

print("\nDiagnostic tests completed.")