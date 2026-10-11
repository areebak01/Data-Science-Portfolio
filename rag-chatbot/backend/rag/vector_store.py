import uuid
import chromadb

from rag.embeddings import generate_embeddings


# Create a persistent local ChromaDB database
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="rag_documents"
)


def store_documents(chunks):
    """Store document chunks with a unique document ID."""

    if not chunks:
        raise ValueError("No text chunks available to store.")

    texts = [chunk.page_content for chunk in chunks]

    embeddings = generate_embeddings(texts)

    document_id = str(uuid.uuid4())

    ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadata = [
        {
            "source": chunk.metadata.get("source", "unknown"),
            "page": chunk.metadata.get("page", 0),
            "document_id": document_id
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadata
    )

    return {
        "document_id": document_id,
        "chunks_stored": len(chunks)
    }


def search_documents(query, document_id, n_results=5):
    """Retrieve relevant chunks from the selected document only."""

    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"document_id": document_id}
    )

    return results


def list_documents():
    """Return unique documents indexed in ChromaDB."""

    results = collection.get(
        include=["metadatas"]
    )

    documents = {}

    for metadata in results["metadatas"]:
        if not metadata:
            continue

        document_id = metadata.get("document_id")
        filename = metadata.get("source")

        if not document_id or not filename:
            continue

        documents[document_id] = {
            "document_id": document_id,
            "filename": filename
        }

    return sorted(
        documents.values(),
        key=lambda document: document["filename"].lower()
    )