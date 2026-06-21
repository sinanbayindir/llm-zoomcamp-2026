import numpy as np
from embedder import Embedder
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index, VectorSearch


QUERY_Q1 = "How does approximate nearest neighbor search work?"
QUERY_Q4 = "What metric do we use to evaluate a search engine?"
QUERY_Q5 = "How do I store vectors in PostgreSQL?"
QUERY_Q6 = "How do I give the model access to tools?"

TARGET_FILE_Q2 = "02-vector-search/lessons/07-sqlitesearch-vector.md"


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


def main():
    embedder = Embedder()

    documents = load_documents()
    chunks = chunk_documents(documents, size=2000, step=1000)

    print("Q1")
    v = embedder.encode(QUERY_Q1)
    print(f"v[0]: {v[0]}")

    print("\nQ2")
    target_doc = next(doc for doc in documents if doc["filename"] == TARGET_FILE_Q2)
    target_vector = embedder.encode(target_doc["content"])
    similarity = v.dot(target_vector)
    print(f"Cosine similarity: {similarity}")

    print("\nEmbedding chunks...")
    chunk_vectors = embedder.encode_batch([chunk["content"] for chunk in chunks])
    X = np.array(chunk_vectors)

    print("\nQ3")
    scores = X.dot(v)
    best_idx = scores.argmax()
    best_chunk = chunks[best_idx]
    print(f"Best filename: {best_chunk['filename']}")
    print(f"Best score: {scores[best_idx]}")

    vector_index = build_vector_index(chunks, X)
    text_index = build_text_index(chunks)

    print("\nQ4")
    q4_vector = embedder.encode(QUERY_Q4)
    q4_results = vector_index.search(q4_vector, num_results=5)
    print(f"First vector result filename: {q4_results[0]['filename']}")
    print("Top 5:")
    for result in q4_results:
        print(result["filename"])

    print("\nQ5")
    q5_vector = embedder.encode(QUERY_Q5)

    q5_vector_results = vector_index.search(q5_vector, num_results=5)
    q5_text_results = text_index.search(query=QUERY_Q5, num_results=5)

    vector_files = {result["filename"] for result in q5_vector_results}
    text_files = {result["filename"] for result in q5_text_results}

    vector_only = vector_files - text_files

    print("Vector top 5:")
    for result in q5_vector_results:
        print(result["filename"])

    print("\nText top 5:")
    for result in q5_text_results:
        print(result["filename"])

    print("\nVector-only files:")
    for filename in vector_only:
        print(filename)

    print("\nQ6")
    q6_vector = embedder.encode(QUERY_Q6)

    q6_vector_results = vector_index.search(q6_vector, num_results=5)
    q6_text_results = text_index.search(query=QUERY_Q6, num_results=5)

    q6_hybrid_results = rrf([q6_vector_results, q6_text_results])

    print(f"First hybrid result filename: {q6_hybrid_results[0]['filename']}")
    print("Hybrid top 5:")
    for result in q6_hybrid_results:
        print(result["filename"])


if __name__ == "__main__":
    main()
