import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "public_health_chunks.jsonl"
)

CHROMA_DIR = PROJECT_DIR / "chroma_db"

COLLECTION_NAME = "public_health_knowledge"

MODEL_NAME = "intfloat/multilingual-e5-small"

BATCH_SIZE = 32


# --------------------------------------------------
# 2. LOAD CHUNKS
# --------------------------------------------------

def load_chunks():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Chunk file not found: {INPUT_FILE}"
        )

    records = []

    with INPUT_FILE.open("r", encoding="utf-8") as file:

        for line in file:

            if line.strip():
                records.append(json.loads(line))

    print(f"Loaded {len(records)} chunks.")

    return records


# --------------------------------------------------
# 3. LOAD EMBEDDING MODEL
# --------------------------------------------------

def load_embedding_model():

    print("\nLoading multilingual embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Embedding model loaded.")

    return model


# --------------------------------------------------
# 4. CREATE CHROMADB COLLECTION
# --------------------------------------------------

def create_collection():

    print("\nConnecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": (
                "Multilingual public health knowledge "
                "base covering six diseases"
            ),
            "hnsw:space": "cosine"
        }
    )

    print("ChromaDB collection ready.")

    return collection


# --------------------------------------------------
# 5. STORE EMBEDDINGS
# --------------------------------------------------

def store_embeddings(records, model, collection):

    total = len(records)

    for start in range(0, total, BATCH_SIZE):

        batch = records[start:start + BATCH_SIZE]

        documents = [
            "passage: " + record["text"]
            for record in batch
        ]

        embeddings = model.encode(
            documents,
            batch_size=16,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        ids = [
            record["chunk_id"]
            for record in batch
        ]

        metadatas = []

        for record in batch:

            metadata = {
                "document_id": str(
                    record.get("document_id") or ""
                ),
                "document_name": str(
                    record.get("document_name") or ""
                ),
                "disease": str(
                    record.get("disease") or "Unknown"
                ),
                "organization": str(
                    record.get("organization") or "Unknown"
                ),
                "source_url": str(
                    record.get("source_url") or ""
                ),
                "page_number": int(
                    record.get("page_number") or 0
                ),
                "extraction_method": str(
                    record.get("extraction_method") or "text"
                ),
                "chunk_index": int(
                    record.get("chunk_index") or 0
                ),
                "start_index": int(
                    record.get("start_index") or 0
                )
            }

            metadatas.append(metadata)

        collection.upsert(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=[
                record["text"] for record in batch
            ],
            metadatas=metadatas
        )

        processed = min(start + BATCH_SIZE, total)

        print(f"Stored {processed}/{total} chunks.")


# --------------------------------------------------
# 6. MAIN
# --------------------------------------------------

def main():

    print("Starting vector database creation...")

    records = load_chunks()

    model = load_embedding_model()

    collection = create_collection()

    store_embeddings(
        records,
        model,
        collection
    )

    print("\n========== DATABASE SUMMARY ==========")

    print("Collection:", COLLECTION_NAME)
    print("Stored chunks:", collection.count())
    print("Database location:", CHROMA_DIR)

    print("======================================")


if __name__ == "__main__":
    main()