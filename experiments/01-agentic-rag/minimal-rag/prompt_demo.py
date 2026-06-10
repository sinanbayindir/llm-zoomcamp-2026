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
    keyword_fields=["course"],
)

index.fit(documents)


query = "When does the course start?"

results = index.search(
    query=query,
    filter_dict={"course": "data-engineering-zoomcamp"},
    num_results=5,
)


context = ""

for doc in results:
    context += f"""
section: {doc["section"]}
question: {doc["question"]}
answer: {doc["text"]}
""".strip()
    context += "\n\n"


prompt = f"""
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT.

Use only the facts from the CONTEXT.
If the CONTEXT doesn't contain the answer, say that you don't know.

QUESTION:
{query}

CONTEXT:
{context}
""".strip()


print(prompt)
