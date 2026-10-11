
from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field

from rag.ingestion import load_and_split_pdf
from rag.vector_store import store_documents, list_documents
from rag.generation import generate_answer


app = FastAPI(
    title="RAG Knowledge Assistant API",
    description="Document Q&A using FastAPI, ChromaDB and Ollama.",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    document_id: str


@app.get("/")
def root():
    return {"message": "RAG Knowledge Assistant API is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/documents")
def get_documents():
    try:
        documents = list_documents()

        return {
            "documents": documents,
            "total": len(documents)
        }

    except Exception as error:
        print(f"Document listing error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve documents."
        )

@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # Save temporarily while processing
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "uploaded.pdf"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Validate PDF signature
        with open(file_path, "rb") as pdf:
            if pdf.read(5) != b"%PDF-":
                raise HTTPException(
                    status_code=400,
                    detail="Invalid PDF file."
                )

        try:
            chunks = load_and_split_pdf(str(file_path))

            if not chunks:
                raise HTTPException(
                    status_code=400,
                    detail="No extractable text found in PDF."
                )

            # Preserve original filename in source metadata
            for chunk in chunks:
                chunk.metadata["source"] = file.filename

            result = store_documents(chunks)

        except HTTPException:
            raise

        except Exception as error:
            print(f"Upload error: {error}")
            raise HTTPException(
                status_code=500,
                detail="Unable to process PDF."
            )

    return {
        "message": "PDF uploaded and indexed successfully.",
        "filename": file.filename,
        **result
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        return generate_answer(
            request.question,
            request.document_id
        )

    except Exception as error:
        print(f"Chat error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Unable to generate an answer."
        )
