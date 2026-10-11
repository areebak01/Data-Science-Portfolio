# RAG Knowledge Assistant

A locally running Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and ask questions about their contents using a local large language model.

The application combines semantic search, vector embeddings and LLM-based answer generation to provide document-grounded responses with page references.

## Features

- Upload and process PDF documents
- Extract and split document text into overlapping chunks
- Generate semantic embeddings using Sentence Transformers
- Store embeddings in a persistent ChromaDB vector database
- Retrieve relevant content from a selected document
- Generate answers using Llama 3.2 through Ollama
- View document sources and page references
- Switch between uploaded documents
- Maintain separate session-based chat histories
- Run the application locally using Docker Compose
- Execute automated tests through GitHub Actions

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Backend API | FastAPI |
| Language model | Llama 3.2 (3B), Ollama |
| Embeddings | all-MiniLM-L6-v2 |
| Vector database | ChromaDB |
| PDF processing | PyPDFLoader, LangChain |
| Programming language | Python 3.11 |
| Containerisation | Docker, Docker Compose |
| Automated testing | Pytest |
| CI | GitHub Actions |

## RAG Architecture

1. A user uploads a PDF through the Streamlit interface.
2. FastAPI extracts the text and divides it into overlapping chunks.
3. Sentence Transformers converts each chunk into a vector embedding.
4. ChromaDB stores the embeddings and associated document metadata.
5. When a question is submitted, the system generates a query embedding.
6. ChromaDB retrieves relevant chunks from the selected document.
7. The retrieved context and question are passed to the local Llama 3.2 model.
8. The generated answer is displayed alongside source page references.

## Running Locally

### Prerequisites

- Python 3.11
- Docker Desktop
- Ollama

Download the language model:

```bash
ollama pull llama3.2:3b
```

Ensure Ollama is running and accessible to the backend.

### Start the application

From the `rag-chatbot` directory:

```bash
docker compose up --build
```

Access the application at:

- Streamlit frontend: http://localhost:8501
- FastAPI documentation: http://localhost:8000/docs

The backend communicates with Ollama running on the host machine. The Docker Compose configuration uses `host.docker.internal`, which is supported by Docker Desktop on macOS.

### Stop the application

Press `Ctrl+C`, or run:

```bash
docker compose down
```

The named Docker volume preserves indexed documents between normal restarts. Running `docker compose down -v` also deletes the volume and its stored data.

## Automated Testing

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the test suite:

```bash
python -m pytest tests/ -v
```

The tests cover API endpoints, request validation, PDF ingestion, and document-specific retrieval. External LLM responses are mocked in API tests, so the automated test suite does not require Ollama to be running.

GitHub Actions runs these tests on pushes and pull requests affecting the project.

## Privacy and Limitations

- The application is intended for local use.
- PDF content and embeddings are stored locally.
- No paid LLM API is required.
- The application does not currently implement user authentication or multi-user access controls.
- PDF upload size limits are not enforced.
- Scanned PDFs without extractable text may require OCR.
- Answers may be inaccurate or incomplete when relevant information is not retrieved.
- Chat histories are session-based and are not persisted across Streamlit sessions.

**Note:** This project is a local prototype and should not be exposed publicly without additional security controls.