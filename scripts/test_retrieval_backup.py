from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = PROJECT_DIR / "chroma_db"

COLLECTION_NAME = "public_health_knowledge"

MODEL_NAME = "intfloat/multilingual-e5-small"


# --------------------------------------------------
# 2. LOAD MODEL AND DATABASE
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("Database records:", collection.count())


# --------------------------------------------------
# 3. RETRIEVAL FUNCTION
# --------------------------------------------------

def search_health_information(question, language):

    query_embedding = model.encode(
        ["query: " + question],
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3
    )

    print(f"\n{'=' * 60}")
    print(f"Language: {language}")
    print(f"Question: {question}")
    print("=" * 60)

    if not results["documents"] or not results["documents"][0]:
        print("No relevant information found.")
        return

    for index, document in enumerate(
        results["documents"][0], start=1
    ):

        metadata = results["metadatas"][0][index - 1]
        distance = results["distances"][0][index - 1]

        similarity = 1 - distance

        print(f"\nResult {index}")
        print("Disease:", metadata["disease"])
        print("Document:", metadata["document_name"])
        print("Page:", metadata["page_number"])
        print("Similarity:", round(similarity, 4))
        print("Source:", metadata["source_url"])
        print("Text:", document[:500])


# --------------------------------------------------
# 4. MULTILINGUAL TEST QUESTIONS
# --------------------------------------------------

test_questions = [
    (
        "What are the symptoms of dengue fever?",
        "English"
    ),
    (
        "డెంగ్యూ జ్వరం లక్షణాలు ఏమిటి?",
        "Telugu"
    ),
    (
        "डेंगू बुखार के लक्षण क्या हैं?",
        "Hindi"
    ),
    (
        "ಡಯಾಬಿಟಿಸ್ ಎಂದರೇನು?",
        "Kannada"
    ),
    (
        "What are the symptoms of tuberculosis?",
        "English"
    ),
    (
        "What causes high blood pressure?",
        "English"
    ),
    (
        "What causes anaemia?",
        "English"
    ),
    (
        "What is malaria and how does it spread?",
        "English"
    )
]


# --------------------------------------------------
# 5. RUN TESTS
# --------------------------------------------------

for question, language in test_questions:

    search_health_information(
        question,
        language
    )


print("\nAll retrieval tests completed.")