import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="P27 Public Health Chatbot",
    page_icon="🏥",
    layout="centered"
)

API_URL = "http://127.0.0.1:8000/api/chat"

DISEASES = [
    "Dengue",
    "Malaria",
    "Tuberculosis",
    "Diabetes",
    "Hypertension",
    "Anaemia"
]

LANGUAGES = [
    "English",
    "Telugu",
    "Hindi",
    "Kannada"
]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page header
st.title("🏥 P27 Public Health Chatbot")

st.markdown(
    """
    Welcome! Ask questions about common diseases
    and preventive healthcare.

    Get simple, multilingual health information
    supported by official public health documents.
    """
)

st.warning(
    "This chatbot provides educational information only. "
    "It does not provide medical diagnosis or replace "
    "a qualified healthcare professional."
)

# Sidebar settings
with st.sidebar:

    st.header("Chat Settings")

    

    selected_language = st.selectbox(
        "Select language",
        LANGUAGES
    )

    st.divider()

    st.subheader("Supported Diseases")

    for disease in DISEASES:
        st.write(f"• {disease}")

    st.divider()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("sources"):

            with st.expander("View sources"):

                for source in message["sources"]:

                    st.write(
                        f"**Document:** {source['document_name']}"
                    )

                    st.write(
                        f"**Page:** {source['page_number']}"
                    )

                    st.markdown(
                        f"[Open source document]({source['source_url']})"
                    )

# Chat input
question = st.chat_input(
    "Ask a public health question..."
)

if question:

    # Save and display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Finding information..."):

            try:

                response = requests.post(
                    API_URL,
                   json={
    "question": question,
    "language": selected_language
},
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)

                if sources:

                    with st.expander("View sources"):

                        for source in sources:

                            st.write(
                                f"**Document:** {source['document_name']}"
                            )

                            st.write(
                                f"**Page:** {source['page_number']}"
                            )

                            st.markdown(
                                f"[Open source document]({source['source_url']})"
                            )

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except requests.exceptions.RequestException as error:

                st.error(
                    "Unable to connect to the chatbot server. "
                    "Please check whether FastAPI is running."
                )

                print(f"API connection error: {error}")