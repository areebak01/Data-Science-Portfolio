
import json
import sys
import time
from pathlib import Path

import requests

API_URL = "http://127.0.0.1:8000/chat"
DATASET_PATH = Path(__file__).parent / "dataset.json"
OUTPUT_PATH = Path(__file__).parent / "answer_results.json"


def main():
    if len(sys.argv) != 2:
        print("Usage: python evaluation/evaluate_answers.py DOCUMENT_ID")
        sys.exit(1)

    document_id = sys.argv[1]

    with open(DATASET_PATH, encoding="utf-8") as file:
        dataset = json.load(file)

    results = []

    for index, item in enumerate(dataset, start=1):
        question = item["question"]
        print(f"\nEvaluating question {index}/{len(dataset)}")
        print(f"Question: {question}", flush=True)

        start = time.perf_counter()

        try:
            response = requests.post(
                API_URL,
                json={
                    "question": question,
                    "document_id": document_id,
                },
                timeout=180,
            )
            response.raise_for_status()
            answer = response.json()["answer"]
        except (requests.RequestException, ValueError, KeyError) as error:
            print(f"Evaluation failed: {error}")
            sys.exit(1)

        latency = round(time.perf_counter() - start, 2)

        keywords = item["expected_keywords"]
        matched_keywords = [
        keyword for keyword in keywords
        if keyword.lower() in answer.lower()
        ]

        if keywords:
            keyword_score = len(matched_keywords) / len(keywords)
            evaluation_type = "answerable"
        else:
            # Check whether the chatbot acknowledges missing information
            refusal_phrases = [
    "does not contain",
    "doesn't contain",
    "does not provide",
    "doesn't provide",
    "does not mention",
    "doesn't mention",
    "not provided",
    "not mentioned",
    "not available",
    "insufficient information",
    "cannot determine",
    "can't determine",
    "doesn't specify",
    "does not specify",
]

            keyword_score = float(
                any(phrase in answer.lower() for phrase in refusal_phrases)
            )
            evaluation_type = "unanswerable"

        results.append({
            "question": question,
            "reference_answer": item["reference_answer"],
            "generated_answer": answer,
            "matched_keywords": matched_keywords,
            "keyword_score": round(keyword_score, 2),
            "latency_seconds": latency,
            "evaluation_type": evaluation_type,
        })

        print(f"Answer: {answer}")
        print(f"Keyword score: {keyword_score:.2f}")
        print(f"Latency: {latency:.2f} seconds")

    average_score = sum(
        result["keyword_score"] for result in results
    ) / len(results)

    average_latency = sum(
        result["latency_seconds"] for result in results
    ) / len(results)

    output = {
        "document_id": document_id,
        "number_of_questions": len(results),
        "average_keyword_score": round(average_score, 2),
        "average_latency_seconds": round(average_latency, 2),
        "results": results,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print("\n--- Evaluation Summary ---")
    print(f"Average keyword score: {average_score:.2f}")
    print(f"Average latency: {average_latency:.2f} seconds")
    print(f"Results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
