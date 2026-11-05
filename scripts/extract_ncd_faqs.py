import json
from pathlib import Path

import pymupdf


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw" / "ncdc"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "ncd_faqs.jsonl"


# Official document details
DOCUMENTS = {
    "diabetes_faqs.pdf": {
        "disease": "Diabetes",
        "organization": "National Centre for Disease Control, MoHFW",
        "source_url": (
            "https://ncdc.mohfw.gov.in/uploads/pdf/"
            "Diabetes%20Mellitus%20English%20FAQs.pdf"
        ),
    },
    "hypertension_faqs.pdf": {
        "disease": "Hypertension",
        "organization": "National Centre for Disease Control, MoHFW",
        "source_url": (
            "https://ncdc.mohfw.gov.in/uploads/pdf/"
            "Hypertension%20English%20FAQs.pdf"
        ),
    },
}


def extract_documents():

    total_pages = 0
    extracted_pages = 0
    skipped_pages = 0

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:

        for filename, metadata in DOCUMENTS.items():

            pdf_path = RAW_DIR / filename

            if not pdf_path.exists():
                print(f"Missing PDF: {filename}")
                continue

            print(f"\nProcessing: {filename}")

            document = pymupdf.open(pdf_path)
            total_pages += len(document)

            for page_number, page in enumerate(document, start=1):

                text = page.get_text("text").strip()

                if len(text) < 30:
                    skipped_pages += 1
                    print(f"  Page {page_number}: insufficient text")
                    continue

                record = {
                    "document_id": pdf_path.stem,
                    "document_name": filename,
                    "disease": metadata["disease"],
                    "organization": metadata["organization"],
                    "source_url": metadata["source_url"],
                    "page_number": page_number,
                    "extraction_method": "text",
                    "text": text,
                }

                output.write(
                    json.dumps(record, ensure_ascii=False) + "\n"
                )

                extracted_pages += 1

            print(f"  Total pages: {len(document)}")
            document.close()

    print("\n========== NCD EXTRACTION SUMMARY ==========")
    print(f"Total pages: {total_pages}")
    print(f"Pages extracted: {extracted_pages}")
    print(f"Pages skipped: {skipped_pages}")
    print(f"Output file: {OUTPUT_FILE}")
    print("============================================")


if __name__ == "__main__":
    extract_documents()