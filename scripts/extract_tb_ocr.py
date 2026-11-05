import json
from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

PROJECT_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "mohfw"
    / "tb_treatment_workflows_2023.pdf"
)

OUTPUT_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "tb_ocr.jsonl"
)

SOURCE_URL = (
    "https://tbcindia.mohfw.gov.in/wp-content/uploads/"
    "2023/05/1874197613Standard-Treatment-Workflows.pdf"
)

ORGANIZATION = (
    "Central TB Division, Ministry of Health and Family Welfare"
)


# --------------------------------------------------
# 2. OCR EXTRACTION FUNCTION
# --------------------------------------------------

def extract_tb_text():

    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found: {PDF_PATH}")
        return

    print("Opening TB PDF...")

    document = pymupdf.open(PDF_PATH)

    total_pages = len(document)
    extracted_pages = 0
    skipped_pages = 0

    print(f"Total PDF pages: {total_pages}")

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_PATH.open("w", encoding="utf-8") as output:

        for page_number, page in enumerate(document, start=1):

            print(
                f"\nProcessing TB page "
                f"{page_number}/{total_pages}..."
            )

            try:

                # Render page at 200 DPI
                pix = page.get_pixmap(
                    dpi=200,
                    alpha=False
                )

                # Convert PDF page into an image
                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                # Extract English text using OCR
                text = pytesseract.image_to_string(
                    image,
                    lang="eng",
                    config="--psm 3"
                ).strip()

                # Skip pages with very little text
                if len(text) < 30:

                    skipped_pages += 1

                    print(
                        "  Very little text detected; "
                        "skipping page."
                    )

                    continue

                # Create structured record
                record = {
                    "document_id": "tb_treatment_workflows_2023",
                    "document_name": PDF_PATH.name,
                    "disease": "Tuberculosis",
                    "organization": ORGANIZATION,
                    "source_url": SOURCE_URL,
                    "page_number": page_number,
                    "extraction_method": "OCR",
                    "text": text
                }

                # Save one JSON record per page
                output.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    ) + "\n"
                )

                extracted_pages += 1

                print(
                    f"  Extracted {len(text)} characters."
                )

            except Exception as error:

                skipped_pages += 1

                print(
                    f"  ERROR on page "
                    f"{page_number}: {error}"
                )

    document.close()

    # --------------------------------------------------
    # 3. EXTRACTION SUMMARY
    # --------------------------------------------------

    print("\n========== TB OCR SUMMARY ==========")

    print(f"Total pages: {total_pages}")
    print(f"Pages extracted: {extracted_pages}")
    print(f"Pages skipped: {skipped_pages}")

    print(f"Output file: {OUTPUT_PATH}")

    print("====================================")


# --------------------------------------------------
# 4. MAIN
# --------------------------------------------------

if __name__ == "__main__":
    extract_tb_text()