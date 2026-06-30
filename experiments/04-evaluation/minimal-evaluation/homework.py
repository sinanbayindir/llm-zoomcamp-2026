import numpy as np
import pandas as pd
from embedder import Embedder
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index, VectorSearch


def load_documents():
    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )

    return [file.parse() for file in reader.read()]


def build_text_index(chunks):
    index = Index(
        text_fields=["content"],
        keyword_fields=["filename"],
    )
    index.fit(chunks)
    return index


def build_vector_index(chunks, X):
    index = VectorSearch(keyword_fields=["filename"])
    index.fit(X, chunks)
    return index


def rrf(result_lists, k=60, num_results=5):
    scores = {}
    docs = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["start"])
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc

    ranked = sorted(scores.keys(), key=lambda key: scores[key], reverse=True)
    return [docs[key] for key in ranked[:num_results]]


def compute_relevance(search_fn, record):
    results = search_fn(record["question"])

    return [
        int(result["filename"] == record["filename"])
        for result in results
    ]


def hit_rate(relevance_total):
    cnt = 0

    for relevance in relevance_total:
        if 1 in relevance:
            cnt += 1

    return cnt / len(relevance_total)


def mrr(relevance_total):
    total_score = 0.0

    for relevance in relevance_total:
        for rank, rel in enumerate(relevance):
            if rel == 1:
                total_score += 1 / (rank + 1)
                break

    return total_score / len(relevance_total)


def evaluate(ground_truth, search_fn):
    relevance_total = []

    for record in ground_truth:
        relevance = compute_relevance(search_fn, record)
        relevance_total.append(relevance)

    return {
        "hit_rate": hit_rate(relevance_total),
        "mrr": mrr(relevance_total),
    }


def main():
    embedder = Embedder()

    documents = load_documents()
    chunks = chunk_documents(documents, size=2000, step=1000)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    ground_truth_df = pd.read_csv("ground-truth.csv")
    ground_truth = ground_truth_df.to_dict(orient="records")

    chunk_vectors = embedder.encode_batch([chunk["content"] for chunk in chunks])
    X = np.array(chunk_vectors)

    text_index = build_text_index(chunks)
    vector_index = build_vector_index(chunks, X)

    def text_search(query, num_results=5):
        return text_index.search(query=query, num_results=num_results)

    def vector_search(query, num_results=5):
        query_vector = embedder.encode(query)
        return vector_index.search(query_vector, num_results=num_results)

    def hybrid_search(query, k=60, num_results=5):
        text_results = text_search(query, num_results=10)
        vector_results = vector_search(query, num_results=10)
        return rrf([text_results, vector_results], k=k, num_results=num_results)

    q = ground_truth[0]["question"]

    print("\nQ2")
    text_results = text_search(q)
    print(f"Question: {q}")
    print(f"First text result: {text_results[0]['filename']}")

    print("\nQ3")
    vector_results = vector_search(q)
    print(f"First vector result: {vector_results[0]['filename']}")

    print("\nQ4")
    text_metrics = evaluate(ground_truth, text_search)
    print(text_metrics)

    print("\nQ5")
    vector_metrics = evaluate(ground_truth, vector_search)
    print(vector_metrics)

    print("\nQ6")
    for k in [1, 50, 100, 200]:
        metrics = evaluate(
            ground_truth,
            lambda query, k=k: hybrid_search(query, k=k),
        )
        print(f"k={k}: {metrics}")


if __name__ == "__main__":
    main()
