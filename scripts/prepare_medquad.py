import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import re

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "medquad"
    / "MedQUAD-master"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "medquad_clean.csv"


def get_text(element):
    """Extract readable text, including text inside nested XML tags."""
    if element is None:
        return ""

    text = " ".join(
        part.strip()
        for part in element.itertext()
        if part and part.strip()
    )

    return re.sub(r"\s+", " ", text).strip()


def get_child(element, name):
    """Find a direct child without depending on XML namespaces."""
    for child in element:
        tag = child.tag.split("}")[-1]

        if tag == name:
            return child

    return None


def process_medquad():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT_DIR.exists():
        raise FileNotFoundError(
            f"MedQuAD folder not found: {INPUT_DIR}"
        )

    xml_files = list(INPUT_DIR.rglob("*.xml"))

    print(f"XML files found: {len(xml_files)}")

    records = []
    seen = set()

    empty_answers = 0
    invalid_records = 0
    failed_files = 0

    for index, xml_file in enumerate(xml_files, start=1):

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            document_id = root.attrib.get("id", "")
            source = root.attrib.get("source", "")
            source_url = root.attrib.get("url", "")

            focus_element = get_child(root, "Focus")
            focus = get_text(focus_element)

            annotations = get_child(root, "FocusAnnotations")
            category_element = None

            if annotations is not None:
                category_element = next(
                    (
                        item
                        for item in annotations.iter()
                        if item.tag.split("}")[-1] == "Category"
                    ),
                    None
                )

            category = get_text(category_element)

            for pair in root.iter():
                if pair.tag.split("}")[-1] != "QAPair":
                    continue

                question_element = get_child(pair, "Question")
                answer_element = get_child(pair, "Answer")

                question = get_text(question_element)
                answer = get_text(answer_element)

                if not answer:
                    empty_answers += 1
                    continue

                if not question or len(answer) < 10:
                    invalid_records += 1
                    continue

                question_type = ""

                if question_element is not None:
                    question_type = question_element.attrib.get(
                        "qtype", ""
                    )

                # Avoid duplicate question-answer combinations
                unique_key = (
                    question.casefold(),
                    answer.casefold()
                )

                if unique_key in seen:
                    continue

                seen.add(unique_key)

                records.append({
                    "document_id": document_id,
                    "source": source,
                    "source_url": source_url,
                    "topic": focus,
                    "category": category,
                    "question_type": question_type,
                    "question": question,
                    "answer": answer,
                })

        except ET.ParseError:
            failed_files += 1
            print(f"XML parsing error: {xml_file}")

        except Exception as error:
            failed_files += 1
            print(f"Error in {xml_file}: {error}")

        if index % 1000 == 0:
            print(f"Processed {index}/{len(xml_files)} files")

    # Save the cleaned dataset
    fieldnames = [
        "document_id",
        "source",
        "source_url",
        "topic",
        "category",
        "question_type",
        "question",
        "answer",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(records)

    print("\n========== MEDQUAD PROCESSING REPORT ==========")
    print(f"XML files discovered: {len(xml_files)}")
    print(f"Valid Q&A records: {len(records)}")
    print(f"Empty answers excluded: {empty_answers}")
    print(f"Invalid records excluded: {invalid_records}")
    print(f"Files with errors: {failed_files}")
    print(f"Output saved to: {OUTPUT_FILE}")
    print("================================================")


if __name__ == "__main__":
    process_medquad()