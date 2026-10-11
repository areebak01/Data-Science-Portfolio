from unittest.mock import patch
from io import BytesIO

def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "RAG Knowledge Assistant API is running!"
    }


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_rejects_empty_question(client):
    response = client.post(
        "/chat",
        json={
            "question": "",
            "document_id": "test-document-id"
        }
    )

    assert response.status_code == 422


def test_chat_requires_document_id(client):
    response = client.post(
        "/chat",
        json={
            "question": "What is the revenue?"
        }
    )

    assert response.status_code == 422

def test_list_documents(client):
    """Check that the API returns indexed documents."""

    fake_documents = [
        {
            "document_id": "test-123",
            "filename": "northstar.pdf"
        }
    ]

    with patch(
        "main.list_documents",
        return_value=fake_documents
    ):
        response = client.get("/documents")

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["documents"] == fake_documents


def test_upload_rejects_non_pdf(client):
    """Reject files with unsupported extensions."""

    response = client.post(
        "/upload",
        files={
            "file": (
                "notes.txt",
                BytesIO(b"Some text"),
                "text/plain"
            )
        }
    )

    assert response.status_code == 400


def test_upload_rejects_invalid_pdf(client):
    """Reject files with a PDF extension but invalid content."""

    response = client.post(
        "/upload",
        files={
            "file": (
                "fake.pdf",
                BytesIO(b"This is not a PDF"),
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400


def test_upload_valid_pdf(client):
    """Check that valid PDFs are processed and indexed."""

    fake_result = {
        "document_id": "test-123",
        "chunks_stored": 2
    }

    with patch(
        "main.load_and_split_pdf",
        return_value=[
            type(
                "Chunk",
                (),
                {
                    "metadata": {},
                    "page_content": "Test content"
                }
            )()
        ]
    ), patch(
        "main.store_documents",
        return_value=fake_result
    ):
        response = client.post(
            "/upload",
            files={
                "file": (
                    "test.pdf",
                    BytesIO(b"%PDF-1.4\nTest"),
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 200
    assert response.json()["document_id"] == "test-123"
    assert response.json()["chunks_stored"] == 2


def test_chat_returns_answer(client):
    """Check that the chat endpoint returns an answer."""

    fake_answer = {
        "answer": "Revenue was GBP 12.4 million.",
        "sources": []
    }

    with patch(
        "main.generate_answer",
        return_value=fake_answer
    ) as mock_generate:

        response = client.post(
            "/chat",
            json={
                "question": "What was the revenue?",
                "document_id": "test-123"
            }
        )

    assert response.status_code == 200
    assert response.json() == fake_answer

    mock_generate.assert_called_once_with(
        "What was the revenue?",
        "test-123"
    )
