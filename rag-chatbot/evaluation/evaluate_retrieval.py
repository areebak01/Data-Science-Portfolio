
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from rag.vector_store import search_documents


def evaluate_retrieval(document_id, top_k=5):
    dataset_path = Path(__file__).parent / "dataset.json"

    with open(dataset_path, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    hits = 0

    for index, example in enumerate(dataset, start=1):
        question = example["question"]
        keywords = example["expected_keywords"]

        results = search_documents(
            query=question,
            document_id=document_id,
            n_results=top_k
        )

        retrieved_chunks = results["documents"][0]

        # A hit occurs when a single chunk contains all keywords.
        hit = any(
            all(keyword.lower() in chunk.lower() for keyword in keywords)
            for chunk in retrieved_chunks
        )

        hits += int(hit)

        print(f"\nQuestion {index}: {question}")
        print(f"Retrieval hit: {hit}")
        print(f"Chunks retrieved: {len(retrieved_chunks)}")

    hit_rate = hits / len(dataset) if dataset else 0

    print(f"\nHit Rate@{top_k}: {hit_rate:.2%}")
    print(f"Questions evaluated: {len(dataset)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluation/evaluate_retrieval.py <document_id>")
        sys.exit(1)

    evaluate_retrieval(sys.argv[1])
