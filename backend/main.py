
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.answer_generator import generate_answer


app = FastAPI(
    title="P27 AI-Driven Public Health Chatbot",
    description="A multilingual, source-grounded public health information chatbot.",
    version="1.0.0"
)


# Allow Streamlit frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost:8502",
        "http://127.0.0.1:8502"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SUPPORTED_DISEASES = [
    "Dengue",
    "Malaria",
    "Tuberculosis",
    "Diabetes",
    "Hypertension",
    "Anaemia"
]


SUPPORTED_LANGUAGES = [
    "English",
    "Telugu",
    "Hindi",
    "Kannada"
]


# Disease names and common multilingual aliases
DISEASE_ALIASES = {
    "Dengue": [
        "dengue",
        "డెంగ్యూ",
        "डेंगू",
        "ಡೆಂಗ್ಯೂ"
    ],

    "Malaria": [
        "malaria",
        "మలేరియా",
        "मलेरिया",
        "ಮಲೇರಿಯಾ"
    ],

    "Tuberculosis": [
        "tuberculosis",
        "tb",
        "క్షయ",
        "टीबी",
        "तपेदिक",
        "ಕ್ಷಯರೋಗ"
    ],

    "Diabetes": [
        "diabetes",
        "diabetic",
        "మధుమేహం",
        "మధుమేహ",
        "मधुमेह",
        "ಸಕ್ಕರೆ ಕಾಯಿಲೆ",
        "ಮಧುಮೇಹ"
    ],

    "Hypertension": [
        "hypertension",
        "high blood pressure",
        "రక్తపోటు",
        "उच्च रक्तचाप",
        "ಅಧಿಕ ರಕ್ತದೊತ್ತಡ"
    ],

    "Anaemia": [
        "anaemia",
        "anemia",
        "low haemoglobin",
        "low hemoglobin",
        "రక్తహీనత",
        "खून की कमी",
        "रक्ताल्पता",
        "ರಕ್ತಹೀನತೆ"
    ]
}


# Automatically identify disease from question
def detect_disease(question: str):

    question_lower = question.casefold()

    matched_diseases = []

    for disease, aliases in DISEASE_ALIASES.items():

        for alias in aliases:

            if alias.casefold() in question_lower:

                matched_diseases.append(disease)
                break

    if len(matched_diseases) == 1:
        return matched_diseases[0]

    if len(matched_diseases) > 1:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Please ask about one disease at a time.",
                "detected_diseases": matched_diseases
            }
        )

    raise HTTPException(
        status_code=400,
        detail={
            "message": (
                "Could not identify the disease from your question. "
                "Please mention one of the supported diseases."
            ),
            "supported_diseases": SUPPORTED_DISEASES
        }
    )


# Request model
class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=3,
        max_length=1000
    )

    disease: str | None = None

    language: str = "English"


# Response model
class ChatResponse(BaseModel):

    answer: str
    disease: str
    language: str
    sources: list[dict]


# Home endpoint
@app.get("/")
def home():

    return {
        "message": "P27 Public Health Chatbot API is running.",
        "status": "healthy"
    }


# Get supported diseases
@app.get("/api/diseases")
def get_diseases():

    return {
        "supported_diseases": SUPPORTED_DISEASES
    }


# Get supported languages
@app.get("/api/languages")
def get_languages():

    return {
        "supported_languages": SUPPORTED_LANGUAGES
    }


# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    question = request.question.strip()
    language = request.language.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Validate language
    matched_language = next(
        (
            item for item in SUPPORTED_LANGUAGES
            if item.casefold() == language.casefold()
        ),
        None
    )

    if not matched_language:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Unsupported language.",
                "supported_languages": SUPPORTED_LANGUAGES
            }
        )

    # Identify disease automatically if not provided
    if request.disease and request.disease.strip():

        disease_input = request.disease.strip()

        matched_disease = next(
            (
                item for item in SUPPORTED_DISEASES
                if item.casefold() == disease_input.casefold()
            ),
            None
        )

        if not matched_disease:

            raise HTTPException(
                status_code=400,
                detail="Unsupported disease category."
            )

    else:

        matched_disease = detect_disease(question)

    # Generate RAG-based answer
    try:

        result = generate_answer(
            question=question,
            disease=matched_disease,
            language=matched_language
        )

        return {
            "answer": result["answer"],
            "disease": matched_disease,
            "language": matched_language,
            "sources": result["sources"]
        }

    except Exception as error:

        print(f"Chat API error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to process your question right now."
        )
