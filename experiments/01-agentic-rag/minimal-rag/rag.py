import requests
from dotenv import load_dotenv
from minsearch import Index
from openai import OpenAI


COURSES_URL = "https://datatalks.club/faq/json/courses.json"
URL_PREFIX = "https://datatalks.club/faq"

load_dotenv()

client = OpenAI()


def load_documents():
    response = requests.get(COURSES_URL)
    response.raise_for_status()

    courses = response.json()
    documents = []

    for course in courses:
        course_url = f"{URL_PREFIX}{course['path']}"
        course_response = requests.get(course_url)
        course_response.raise_for_status()

        course_documents = course_response.json()
        documents.extend(course_documents)

    return documents


def build_index(documents):
    index = Index(
        text_fields=["question", "section", "answer"],
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
answer: {doc["answer"]}
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
