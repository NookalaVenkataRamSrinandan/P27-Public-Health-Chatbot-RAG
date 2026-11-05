import json
import re
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "public_health_combined.jsonl"
)

OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "public_health_chunks.jsonl"
)


# --------------------------------------------------
# 2. SOURCE URLS
# --------------------------------------------------

SOURCE_URLS = {
    "dengue_guidelines_2023.pdf":
        "https://ncvbdc.mohfw.gov.in/Doc/National%20Guidelines%20for%20Clinical%20Management%20of%20Dengue%20Fever%202023.pdf",

    "malaria_training_2025.pdf":
        "https://ncvbdc.mohfw.gov.in/Doc/Malaria-Training-Module-ASHA-2025.pdf",

    "tb_treatment_workflows_2023.pdf":
        "https://tbcindia.mohfw.gov.in/wp-content/uploads/2023/05/1874197613Standard-Treatment-Workflows.pdf",

    "anemia_mukt_bharat_guidelines.pdf":
        "https://resource.anemiamuktbharat.info/Operational%20Guideline/Operational%20Guideline/Anemia-Mukt-Bharat-Operational-Guidelines-FINAL.pdf",

    "diabetes_faqs.pdf":
        "https://ncdc.mohfw.gov.in/uploads/pdf/Diabetes%20Mellitus%20English%20FAQs.pdf",

    "hypertension_faqs.pdf":
        "https://ncdc.mohfw.gov.in/uploads/pdf/Hypertension%20English%20FAQs.pdf",
}


# --------------------------------------------------
# 3. TEXT CLEANING
# --------------------------------------------------

def clean_text(text):

    if not isinstance(text, str):
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# --------------------------------------------------
# 4. CHUNKING CONFIGURATION
# --------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=150,
    length_function=len,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ],
    add_start_index=True
)


# --------------------------------------------------
# 5. PROCESS DOCUMENTS
# --------------------------------------------------

def create_chunks():

    if not INPUT_FILE.exists():
        print(f"Input file not found: {INPUT_FILE}")
        return

    total_records = 0
    total_chunks = 0
    skipped_short_chunks = 0

    disease_counts = {}
    document_counts = {}

    with INPUT_FILE.open("r", encoding="utf-8") as source, \
            OUTPUT_FILE.open("w", encoding="utf-8") as output:

        for line in source:

            if not line.strip():
                continue

            record = json.loads(line)
            total_records += 1

            cleaned_text = clean_text(
                record.get("text", "")
            )

            if not cleaned_text:
                continue

            chunks = text_splitter.create_documents(
                texts=[cleaned_text]
            )

            for chunk_index, chunk in enumerate(chunks):

                chunk_text = chunk.page_content.strip()

                # Skip very short or incomplete chunks
                if len(chunk_text) < 100:
                    skipped_short_chunks += 1
                    continue

                document_name = record.get(
                    "document_name",
                    "unknown"
                )

                source_url = (
                    record.get("source_url")
                    or SOURCE_URLS.get(document_name, "")
                )

                chunk_record = {
                    "chunk_id": (
                        f"{record.get('document_id', 'doc')}"
                        f"_page_{record.get('page_number', 0)}"
                        f"_chunk_{chunk_index + 1}"
                    ),

                    "document_id": record.get("document_id"),
                    "document_name": document_name,
                    "disease": record.get(
                        "disease",
                        "Unknown"
                    ),
                    "organization": record.get(
                        "organization",
                        "Unknown"
                    ),
                    "source_url": source_url,
                    "page_number": record.get("page_number"),
                    "extraction_method": record.get(
                        "extraction_method",
                        "text"
                    ),
                    "chunk_index": chunk_index,
                    "start_index": chunk.metadata.get(
                        "start_index",
                        0
                    ),
                    "text": chunk_text
                }

                output.write(
                    json.dumps(
                        chunk_record,
                        ensure_ascii=False
                    ) + "\n"
                )

                total_chunks += 1

                disease = chunk_record["disease"]

                disease_counts[disease] = (
                    disease_counts.get(disease, 0) + 1
                )

                document_counts[document_name] = (
                    document_counts.get(document_name, 0) + 1
                )

    # --------------------------------------------------
    # 6. EXTRACTION SUMMARY
    # --------------------------------------------------

    print("\n========== CHUNKING SUMMARY ==========")

    print(f"Input records: {total_records}")
    print(f"Total chunks: {total_chunks}")
    print(f"Short chunks skipped: {skipped_short_chunks}")

    print("\nChunks by disease:")

    for disease, count in sorted(disease_counts.items()):
        print(f"{disease}: {count}")

    print("\nChunks by document:")

    for document, count in sorted(document_counts.items()):
        print(f"{document}: {count}")

    print(f"\nOutput file: {OUTPUT_FILE}")

    print("======================================")


# --------------------------------------------------
# 7. MAIN
# --------------------------------------------------

if __name__ == "__main__":
    create_chunks()