# P27 – AI-Driven Public Health Chatbot

A multilingual, AI-powered public health chatbot that uses **Retrieval-Augmented Generation (RAG)** to provide reliable, source-grounded health information.

## Project Overview

The AI-Driven Public Health Chatbot is designed to make public health information more accessible through a conversational interface. It retrieves relevant information from a curated knowledge base and uses a language model to generate context-aware responses.

The project focuses on six common health conditions and supports multiple Indian languages.

## Key Features

- **Multilingual support:** English, Telugu, Hindi and Kannada.
- **Six health topics:** Dengue, Malaria, Tuberculosis (TB), Diabetes, Hypertension and Anaemia.
- **RAG-based responses:** Retrieves relevant information before generating answers.
- **Source-grounded information:** Uses a curated public health knowledge base.
- **Conversational interface:** Allows users to ask health-related questions in natural language.
- **REST API:** FastAPI backend for handling chatbot requests.

## Supported Health Conditions

| Disease | Coverage |
|---|---|
| Dengue | Public health information |
| Malaria | Public health information |
| Tuberculosis | Public health information |
| Diabetes | Public health information |
| Hypertension | Public health information |
| Anaemia | Public health information |

## Languages Supported

- English
- Telugu
- Hindi
- Kannada

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Vector Database | ChromaDB |
| Embedding Model | multilingual-e5-small |
| Language Model | Groq |
| RAG Framework | Retrieval-Augmented Generation |

## System Architecture

The chatbot follows a Retrieval-Augmented Generation workflow:

1. User submits a health-related question.
2. The question is converted into an embedding.
3. The retriever searches the ChromaDB knowledge base for relevant information.
4. Retrieved context is passed to the language model.
5. The model generates a response grounded in the retrieved information.
6. The response is returned to the user through the chatbot interface.

## Project Structure

```text
P27_Public_Health_Chatbot/
│
├── backend/
│   ├── __init__.py
│   ├── answer_generator.py
│   ├── main.py
│   └── retriever.py
│
├── data/
│   └── processed/
│       ├── ncd_faqs.jsonl
│       ├── public_health_chunks.jsonl
│       ├── public_health_combined.jsonl
│       ├── public_health_documents.jsonl
│       └── tb_ocr.jsonl
│
├── frontend/
│   └── app.py
│
├── scripts/
│   ├── build_vector_database.py
│   ├── chunk_public_health_data.py
│   ├── diagnose_retrieval.py
│   ├── extract_ncd_faqs.py
│   ├── extract_public_health_pdfs.py
│   ├── extract_tb_ocr.py
│   ├── merge_public_health_data.py
│   ├── prepare_medquad.py
│   └── ...
│
├── .gitignore
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/NookalaVenkataRamSrinandan/P27-Public-Health-Chatbot-RAG.git
cd P27-Public-Health-Chatbot-RAG
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your Groq API credentials:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Never upload your actual API key or `.env` file to GitHub.

### 5. Build the vector database

```bash
python scripts/build_vector_database.py
```

### 6. Start the backend

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Backend API documentation:

`http://127.0.0.1:8000/docs`

### 7. Start the frontend

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/app.py
```

## Data Sources

The project knowledge base is built using public health FAQs and health-related government resources, including Indian public health documents.

The repository includes processed knowledge-base files. Raw datasets and source documents may be subject to their respective licences and redistribution conditions.

## Limitations

- The chatbot is an academic prototype and has not been clinically validated.
- Generated responses may contain inaccuracies.
- The quality of responses depends on the available knowledge base and retrieved context.
- The chatbot must not be used as a substitute for professional medical advice, diagnosis or treatment.

## Disclaimer

**This chatbot is intended for educational and informational purposes only.** It is not a medical diagnostic tool and does not replace consultation with qualified healthcare professionals. Always seek professional medical advice for health concerns.

## Project Information

**Project:** P27 – AI-Driven Public Health Chatbot  
**Domain:** Artificial Intelligence and Machine Learning  
**Core Approach:** Retrieval-Augmented Generation (RAG)  
**Repository:** [P27 Public Health Chatbot on GitHub](https://github.com/NookalaVenkataRamSrinandan/P27-Public-Health-Chatbot-RAG)