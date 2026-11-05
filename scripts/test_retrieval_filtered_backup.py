from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_DIR / "chroma_db"
COLLECTION_NAME = "public_health_knowledge"
MODEL_NAME = "intfloat/multilingual-e5-small"

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

print("Connecting to ChromaDB...")
client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_collection(name=COLLECTION_NAME)

print("Database records:", collection.count())


def search_health_information(question, language, disease):
    query_embedding = model.encode(
        ["query: " + question],
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3,
        where={"disease": disease}
    )

    print("\n" + "=" * 60)
    print("Language:", language)
    print("Disease filter:", disease)
    print("Question:", question)
    print("=" * 60)

    if not results["documents"] or not results["documents"][0]:
        print("No relevant information found.")
        return

    for index, document in enumerate(results["documents"][0], start=1):
        metadata = results["metadatas"][0][index - 1]
        distance = results["distances"][0][index - 1]

        print(f"\nResult {index}")
        print("Disease:", metadata["disease"])
        print("Document:", metadata["document_name"])
        print("Page:", metadata["page_number"])
        print("Similarity:", round(1 - distance, 4))
        print("Source:", metadata["source_url"])
        print("Text:", document[:500])


test_questions = [
    ("What are the symptoms of dengue fever?", "English", "Dengue"),
    ("డెంగ్యూ జ్వరం లక్షణాలు ఏమిటి?", "Telugu", "Dengue"),
    ("डेंगू बुखार के लक्षण क्या हैं?", "Hindi", "Dengue"),
    ("ಡಯಾಬಿಟಿಸ್ ಎಂದರೇನು?", "Kannada", "Diabetes"),
    ("What are the symptoms of tuberculosis?", "English", "Tuberculosis"),
    ("What causes high blood pressure?", "English", "Hypertension"),
    ("What causes anaemia?", "English", "Anaemia"),
    ("What is malaria and how does it spread?", "English", "Malaria")
]


for question, language, disease in test_questions:
    search_health_information(question, language, disease)


print("\nAll disease-filtered retrieval tests completed.")