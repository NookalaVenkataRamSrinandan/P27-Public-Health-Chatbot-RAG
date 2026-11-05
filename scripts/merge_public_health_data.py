import json
from pathlib import Path
from collections import Counter

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

SOURCE_FILES = [
    PROCESSED_DIR / "public_health_documents.jsonl",
    PROCESSED_DIR / "tb_ocr.jsonl",
    PROCESSED_DIR / "ncd_faqs.jsonl",
]

OUTPUT_FILE = PROCESSED_DIR / "public_health_combined.jsonl"


def merge_documents():

    total_records = 0
    disease_counts = Counter()
    missing_files = []

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:

        for source_file in SOURCE_FILES:

            if not source_file.exists():
                missing_files.append(source_file.name)
                print(f"Missing file: {source_file.name}")
                continue

            print(f"\nReading: {source_file.name}")

            with source_file.open("r", encoding="utf-8") as source:

                for line in source:

                    if not line.strip():
                        continue

                    record = json.loads(line)

                    disease = record.get("disease", "Unknown")

                    output.write(
                        json.dumps(record, ensure_ascii=False) + "\n"
                    )

                    total_records += 1
                    disease_counts[disease] += 1

    print("\n========== MERGE SUMMARY ==========")
    print(f"Total records: {total_records}")

    for disease, count in sorted(disease_counts.items()):
        print(f"{disease}: {count}")

    if missing_files:
        print("Missing files:", missing_files)

    print(f"\nOutput file: {OUTPUT_FILE}")
    print("===================================")


if __name__ == "__main__":
    merge_documents()