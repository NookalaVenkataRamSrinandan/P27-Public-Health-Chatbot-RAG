import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from backend.answer_generator import generate_answer


def main():

    question = "What are the symptoms of dengue?"
    disease = "Dengue"

    print("=" * 60)
    print("P27 PUBLIC HEALTH CHATBOT - RAG TEST")
    print("=" * 60)

    print(f"\nQuestion: {question}")
    print(f"Disease: {disease}")

    result = generate_answer(
        question=question,
        disease=disease
    )

    print("\nGenerated Answer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(f"\nDocument: {source['document_name']}")
        print(f"Page: {source['page_number']}")
        print(f"URL: {source['source_url']}")

    print("\n" + "=" * 60)
    print("RAG TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()