import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the project root
PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def main():

    if not API_KEY:
        print("ERROR: GROQ_API_KEY not found in .env")
        return

    print("Connecting to Groq...")
    print(f"Model: {MODEL_NAME}")

    try:
        client = Groq(api_key=API_KEY)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a public health education assistant. "
                        "Provide simple, accurate, educational information. "
                        "Do not diagnose diseases or prescribe treatment."
                    )
                },
                {
                    "role": "user",
                    "content": "In two simple sentences, explain what dengue is."
                }
            ],
            temperature=0.3,
            max_tokens=200
        )

        answer = response.choices[0].message.content

        print("\nGroq API connection successful!")
        print("\nGenerated answer:")
        print(answer)

    except Exception as error:
        print("\nGroq API test failed.")
        print(f"Error type: {type(error).__name__}")
        print(f"Error details: {error}")


if __name__ == "__main__":
    main()