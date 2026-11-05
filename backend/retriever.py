from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = PROJECT_DIR / "chroma_db"
COLLECTION_NAME = "public_health_knowledge"
MODEL_NAME = "intfloat/multilingual-e5-small"

print("Loading retrieval model...")

embedding_model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


def retrieve_information(question: str, disease: str, top_k: int = 5):

    query_embedding = embedding_model.encode(
        ["query: " + question],
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        where={"disease": disease}
    )

    retrieved_chunks = []

    if not results["documents"] or not results["documents"][0]:
        return retrieved_chunks

    for index, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][index]
        distance = results["distances"][0][index]

        retrieved_chunks.append({
            "text": document,
            "disease": metadata["disease"],
            "document_name": metadata["document_name"],
            "page_number": metadata["page_number"],
            "source_url": metadata["source_url"],
            "similarity": round(1 - distance, 4)
        })

    return retrieved_chunks