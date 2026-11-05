from pathlib import Path
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not API_KEY:
    raise ValueError("Gemini API key not found.")

client = genai.Client(api_key=API_KEY)

MAX_ATTEMPTS = 4

for attempt in range(1, MAX_ATTEMPTS + 1):

    try:
        print(f"\nGemini connection attempt {attempt}/{MAX_ATTEMPTS}")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=(
                "Explain dengue in two simple sentences. "
                "Do not provide diagnosis or treatment instructions."
            )
        )

        print("\nGemini response:")
        print(response.text)
        print("\nGemini API test successful!")
        break

    except errors.ServerError as error:
        print("Temporary server error:", error)

        if attempt == MAX_ATTEMPTS:
            print("Gemini is still unavailable. Try again later.")
            break

        wait_time = 2 ** attempt
        print(f"Retrying in {wait_time} seconds...")
        time.sleep(wait_time)

    except Exception as error:
        print("Request failed:", type(error).__name__, str(error))
        break