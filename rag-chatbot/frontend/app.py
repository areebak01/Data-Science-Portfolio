
import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="RAG Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)


# Initialise session state

if "documents" not in st.session_state:
    st.session_state.documents = {}

if "active_document_id" not in st.session_state:
    st.session_state.active_document_id = None

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}


def load_documents():
    """Fetch previously indexed PDFs from FastAPI."""
    response = requests.get(
        f"{API_URL}/documents",
        timeout=15
    )
    response.raise_for_status()

    data = response.json()

    st.session_state.documents = {
        document["document_id"]: document["filename"]
        for document in data["documents"]
    }

    # Create an empty chat history for newly discovered PDFs
    for document_id in st.session_state.documents:
        if document_id not in st.session_state.chat_histories:
            st.session_state.chat_histories[document_id] = []

    # Select a valid document
    if (
        st.session_state.active_document_id
        not in st.session_state.documents
    ):
        st.session_state.active_document_id = (
            next(iter(st.session_state.documents), None)
        )


try:
    load_documents()

except requests.RequestException as error:
    st.warning(
        "Unable to load saved documents. "
        "Check that FastAPI is running."
    )


if "active_document_id" not in st.session_state:
    st.session_state.active_document_id = None

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}


# Sidebar
with st.sidebar:
    st.title("📚 Document Assistant")
    st.write("Upload PDFs and ask questions about their contents.")

    uploaded_file = st.file_uploader(
        "Choose a PDF document",
        type=["pdf"]
    )

    if uploaded_file is not None:
        if st.button("Process Document", type="primary"):
            with st.spinner("Processing your document..."):
                try:
                    response = requests.post(
                        f"{API_URL}/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf"
                            )
                        },
                        timeout=180
                    )

                    response.raise_for_status()
                    data = response.json()

                    document_id = data["document_id"]
                    filename = data["filename"]

                    st.session_state.documents[document_id] = filename
                    st.session_state.chat_histories[document_id] = []
                    st.session_state.active_document_id = document_id

                    st.success("Document processed successfully!")

                except requests.RequestException as error:
                    st.error(f"Upload failed: {error}")

    # Document library
    if st.session_state.documents:
        st.divider()
        st.subheader("Document Library")

        document_ids = list(st.session_state.documents.keys())

        selected_id = st.selectbox(
            "Select a document",
            options=document_ids,
            index=document_ids.index(
                st.session_state.active_document_id
            ),
            format_func=lambda doc_id: (
                st.session_state.documents[doc_id]
            )
        )

        st.session_state.active_document_id = selected_id

        st.caption(
            f"{len(document_ids)} document(s) uploaded"
        )

        if st.button("Clear Current Chat"):
            st.session_state.chat_histories[selected_id] = []
            st.rerun()


# Main interface
st.title("AI Knowledge Assistant")
st.caption("Powered by Llama 3.2, ChromaDB, FastAPI and Streamlit")

active_id = st.session_state.active_document_id

if active_id is None:
    st.info(
        "Upload and process a PDF using the sidebar "
        "to get started."
    )

else:
    active_filename = st.session_state.documents[active_id]

    st.info(f"📄 Active document: {active_filename}")

    messages = st.session_state.chat_histories[active_id]

    # Display chat history
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("View Sources"):
                    unique_sources = {
                        (source["source"], source["page"])
                        for source in message["sources"]
                    }

                    for filename, page in sorted(unique_sources):
                        st.write(
                            f"📄 {filename} — Page {page + 1}"
                        )

    # Chat input
    question = st.chat_input(
        "Ask a question about your document..."
    )

    if question:
        messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={
                            "question": question,
                            "document_id": active_id
                        },
                        timeout=180
                    )

                    response.raise_for_status()
                    result = response.json()

                    answer = result["answer"]
                    sources = result.get("sources", [])

                    st.markdown(answer)

                    if sources:
                        with st.expander("View Sources"):
                            unique_sources = {
                                (source["source"], source["page"])
                                for source in sources
                            }

                            for filename, page in sorted(unique_sources):
                                st.write(
                                    f"📄 {filename} — Page {page + 1}"
                                )

                    messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except requests.RequestException as error:
                    st.error(
                        f"Unable to generate answer: {error}"
                    )
