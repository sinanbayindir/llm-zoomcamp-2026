import requests

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

print(f"Total documents: {len(documents)}")
print(documents[0])
