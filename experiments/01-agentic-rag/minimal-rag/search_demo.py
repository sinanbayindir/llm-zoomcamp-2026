import requests
from minsearch import Index


docs_url = "https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json"

response = requests.get(docs_url)
response.raise_for_status()

raw_documents = response.json()

documents = []

for course in raw_documents:
    course_name = course["course"]

    for doc in course["documents"]:
        doc["course"] = course_name
        documents.append(doc)


index = Index(
    text_fields=["question", "text", "section"],
    keyword_fields=["course"]
)

index.fit(documents)


query = "When does the course start?"

results = index.search(
    query=query,
    filter_dict={"course": "data-engineering-zoomcamp"},
    num_results=5
)

for idx, doc in enumerate(results, start=1):
    print(f"\nRESULT {idx}")
    print("-" * 50)
    print(f"QUESTION: {doc['question']}")
    print(f"SECTION : {doc['section']}")
    print(f"COURSE : {doc['course']}")
    print(f"TEXT    : {doc['text'][:300]}")
