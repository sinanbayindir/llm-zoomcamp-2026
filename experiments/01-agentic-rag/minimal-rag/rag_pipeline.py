import requests
from dotenv import load_dotenv
from minsearch import Index
from openai import OpenAI


load_dotenv()

client = OpenAI()


def load_documents():
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

    return documents


def build_index(documents):
    index = Index(
        text_fields=["question", "text", "section"],
        keyword_fields=["course"],
    )

    index.fit(documents)

    return index


def search(index, query, course):
    return index.search(
        query=query,
        filter_dict={"course": course},
        num_results=5,
    )


def build_prompt(query, search_results):
    context = ""

    for doc in search_results:
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

    return prompt


def llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content


def rag(query, course):
    documents = load_documents()
    index = build_index(documents)
    search_results = search(index, query, course)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)

    return answer


if __name__ == "__main__":
    question = "When does the course start?"
    course_name = "data-engineering-zoomcamp"

    answer = rag(question, course_name)
    print(answer)
