
from unittest.mock import patch

from rag.vector_store import search_documents


def test_search_filters_by_document_id():
    """Search must filter results by the selected document."""

    fake_results = {
        "documents": [["Northstar revenue was GBP 12.4 million."]],
        "metadatas": [[{
            "document_id": "northstar-123",
            "source": "northstar.pdf",
            "page": 0
        }]],
        "ids": [["chunk-1"]]
    }

    with patch(
        "rag.vector_store.generate_embeddings",
        return_value=[[0.1, 0.2, 0.3]]
    ), patch(
        "rag.vector_store.collection"
    ) as mock_collection:

        mock_collection.query.return_value = fake_results

        results = search_documents(
            query="What was the revenue?",
            document_id="northstar-123",
            n_results=5
        )

        mock_collection.query.assert_called_once_with(
            query_embeddings=[[0.1, 0.2, 0.3]],
            n_results=5,
            where={"document_id": "northstar-123"}
        )

        assert results["documents"][0][0] == (
            "Northstar revenue was GBP 12.4 million."
        )


def test_search_uses_selected_document():
    """Different document IDs must produce different filters."""

    with patch(
        "rag.vector_store.generate_embeddings",
        return_value=[[0.1, 0.2, 0.3]]
    ), patch(
        "rag.vector_store.collection"
    ) as mock_collection:

        mock_collection.query.return_value = {
            "documents": [[]],
            "metadatas": [[]]
        }

        search_documents(
            query="What is the revenue?",
            document_id="document-A"
        )

        search_documents(
            query="What is the revenue?",
            document_id="document-B"
        )

        calls = mock_collection.query.call_args_list

        assert calls[0].kwargs["where"] == {
            "document_id": "document-A"
        }

        assert calls[1].kwargs["where"] == {
            "document_id": "document-B"
        }
