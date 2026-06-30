import json
from statistics import mean

from dotenv import load_dotenv
from gitsource import GithubRepositoryDataReader
from openai import OpenAI
from pydantic import BaseModel


MODEL = "gpt-5.4-mini"

TARGET_FILES = [
    "01-agentic-rag/lessons/01-intro.md",
    "01-agentic-rag/lessons/02-environment.md",
    "01-agentic-rag/lessons/03-rag.md",
]

DATA_GEN_INSTRUCTIONS = """
You emulate a student who is taking our LLM course.
You are given one lesson page from the course.
Formulate 5 questions this student might ask that are answered by this page.

Rules:
- The page should contain the answer to each question.
- Make the questions complete and not too short.
- Use as few words as possible from the page; don't copy its phrasing.
- The questions should resemble how people actually ask things online:
  not too formal, not too short, not too long.
- Ask about the content of the lesson, not about its formatting or filename.
""".strip()


class Questions(BaseModel):
    questions: list[str]


load_dotenv()
client = OpenAI()


def load_documents() -> list[dict]:
    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )

    return [file.parse() for file in reader.read()]


def generate_questions(document: dict):
    user_prompt = json.dumps(
        {
            "filename": document["filename"],
            "content": document["content"],
        },
        ensure_ascii=False,
    )

    response = client.responses.parse(
        model=MODEL,
        instructions=DATA_GEN_INSTRUCTIONS,
        input=user_prompt,
        text_format=Questions,
    )

    if response.usage is None:
        raise RuntimeError("No usage returned by OpenAI API")

    return response


def main() -> None:
    documents = load_documents()

    selected_documents = [
        document
        for document in documents
        if document["filename"] in TARGET_FILES
    ]

    input_tokens: list[int] = []

    for document in selected_documents:
        response = generate_questions(document)

        if response.usage is None:
            raise RuntimeError("No usage returned by OpenAI API")

        usage = response.usage

        print(f"\nFile: {document['filename']}")
        print(f"Input tokens: {usage.input_tokens}")
        print(response.output_parsed)

        input_tokens.append(usage.input_tokens)

    avg_input_tokens = mean(input_tokens)

    print("\nQ1")
    print(f"Input tokens: {input_tokens}")
    print(f"Average input tokens: {avg_input_tokens}")


if __name__ == "__main__":
    main()
