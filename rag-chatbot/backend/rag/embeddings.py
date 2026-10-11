
from sentence_transformers import SentenceTransformer

# Load a lightweight embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(texts):
    """
    Convert a list of text strings into vector embeddings.
    """
    embeddings = model.encode(texts)

    return embeddings.tolist()
