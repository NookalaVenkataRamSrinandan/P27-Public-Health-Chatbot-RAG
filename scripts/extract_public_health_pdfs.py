import json
from pathlib import Path

import pymupdf

# Project directories
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "public_health_documents.jsonl"

# Document metadata
DOCUMENT_INFO = {
    "dengue_guidelines_2023.pdf": {
        "disease": "Dengue",
        "organization": "NCVBDC, Ministry of Health and Family Welfare",
    },
    "malaria_training_2025.pdf": {
        "disease": "Malaria",
        "organization": "NCVBDC, Ministry of Health and Family Welfare",
    },
    "tb_treatment_workflows_2023.pdf": {
        "disease": "Tuberculosis",
        "organization": "Central TB Division, Ministry of Health and Family Welfare",
    },
    "anemia_mukt_bharat_guidelines.pdf": {
        "disease": "Anaemia",
        "organization": "Anemia Mukt Bharat",
    },
}


def extract_pdf_text():
    pdf_files = list(RAW_DIR.rglob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    total_pages = 0
    extracted_pages = 0
    empty_pages = 0

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:

        for pdf_path in pdf_files:
            print(f"\nProcessing: {pdf_path.name}")

            try:
                document = pymupdf.open(pdf_path)

                info = DOCUMENT_INFO.get(
                    pdf_path.name,
                    {
                        "disease": "Unclassified",
                        "organization": "Unknown",
                    },
                )

                for page_number, page in enumerate(document, start=1):
                    total_pages += 1

                    text = page.get_text("text").strip()

                    if len(text) < 50:
                        empty_pages += 1
                        continue

                    record = {
                        "document_id": pdf_path.stem,
                        "document_name": pdf_path.name,
                        "disease": info["disease"],
                        "organization": info["organization"],
                        "page_number": page_number,
                        "text": text,
                    }

                    output.write(
                        json.dumps(record, ensure_ascii=False) + "\n"
                    )

                    extracted_pages += 1

                document.close()

                print(
                    f"  Pages: {len(pymupdf.open(pdf_path))}"
                )

            except Exception as error:
                print(f"  ERROR: {error}")

    print("\n========== EXTRACTION SUMMARY ==========")
    print(f"Total PDF pages: {total_pages}")
    print(f"Pages extracted: {extracted_pages}")
    print(f"Pages skipped: {empty_pages}")
    print(f"Output file: {OUTPUT_FILE}")
    print("========================================")


if __name__ == "__main__":
    extract_pdf_text()