import sys
from pathlib import Path

# Add the project root directory to Python's import path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

# Import the retrieval function
from backend.retriever import retrieve_information


def main():

    # Test questions for all six diseases
    test_cases = [
        ("What are the symptoms of dengue?", "Dengue"),
        ("How does malaria spread?", "Malaria"),
        ("What are the symptoms of tuberculosis?", "Tuberculosis"),
        ("What causes diabetes?", "Diabetes"),
        ("What are the causes of hypertension?", "Hypertension"),
        ("What causes anaemia?", "Anaemia"),
    ]

    # Run retrieval tests
    for question, disease in test_cases:

        print("\n" + "=" * 70)
        print(f"Disease: {disease}")
        print(f"Question: {question}")

        try:
            results = retrieve_information(
                question=question,
                disease=disease,
                top_k=3
            )

            print(f"\nRetrieved chunks: {len(results)}")

            if not results:
                print("No relevant information retrieved.")
                continue

            for index, result in enumerate(results, start=1):

                print(f"\nResult {index}")
                print(f"Document: {result['document_name']}")
                print(f"Page: {result['page_number']}")
                print(f"Similarity: {result['similarity']}")
                print(f"Text: {result['text'][:350]}")

        except Exception as error:
            print(f"Error while testing {disease}: {error}")

    print("\n" + "=" * 70)
    print("All disease retrieval tests completed.")


if __name__ == "__main__":
    main()