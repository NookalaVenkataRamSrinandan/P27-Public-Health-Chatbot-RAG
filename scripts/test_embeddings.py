from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. LOAD MULTILINGUAL MODEL
# --------------------------------------------------

MODEL_NAME = "intfloat/multilingual-e5-small"

print("Loading multilingual embedding model...")
print("First download may take a few minutes.")

model = SentenceTransformer(MODEL_NAME)

print("Model loaded successfully!")


# --------------------------------------------------
# 2. ENGLISH HEALTH DOCUMENT
# --------------------------------------------------

health_document = (
    "Dengue is a mosquito-borne viral disease. "
    "Common symptoms include high fever, headache, "
    "muscle pain, joint pain and skin rash. "
    "Prevent mosquito bites and seek medical advice "
    "if symptoms develop."
)


# --------------------------------------------------
# 3. MULTILINGUAL TEST QUERIES
# --------------------------------------------------

queries = {
    "English": "query: What are the symptoms of dengue fever?",

    "Telugu": "query: డెంగ్యూ జ్వరం లక్షణాలు ఏమిటి?",

    "Hindi": "query: डेंगू बुखार के लक्षण क्या हैं?",

    "Kannada": "query: ಡೆಂಗ್ಯೂ ಜ್ವರದ ಲಕ್ಷಣಗಳು ಯಾವುವು?"
}


# --------------------------------------------------
# 4. GENERATE EMBEDDINGS
# --------------------------------------------------

print("\nGenerating document embedding...")

document_embedding = model.encode(
    ["passage: " + health_document],
    normalize_embeddings=True
)

print("Generating multilingual query embeddings...")

query_embeddings = model.encode(
    list(queries.values()),
    normalize_embeddings=True
)


# --------------------------------------------------
# 5. CALCULATE SIMILARITY
# --------------------------------------------------

similarities = cosine_similarity(
    query_embeddings,
    document_embedding
).flatten()


# --------------------------------------------------
# 6. DISPLAY RESULTS
# --------------------------------------------------

print("\n========== MULTILINGUAL TEST RESULTS ==========")

for language, score in zip(queries.keys(), similarities):

    print(f"{language}: Similarity = {score:.4f}")

print("\nEmbedding dimensions:", document_embedding.shape[1])

print("All embedding tests completed.")

print("================================================")