import json
from typing import Any, cast

from dotenv import load_dotenv
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index
from openai import OpenAI


MODEL = "gpt-5.4-mini"

QUESTION = "How does the agentic loop work, and how is it different from plain RAG?"

INSTRUCTIONS = """
You're a course teaching assistant. Answer the student's question using the
search tool. Make multiple searches with different keywords before answering.
""".strip()

load_dotenv()
client = OpenAI()


def load_documents() -> list[dict[str, Any]]:
    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )

    files = reader.read()
    return [file.parse() for file in files]


documents = load_documents()
chunks = chunk_documents(documents, size=2000, step=1000)

index = Index(
    text_fields=["content"],
    keyword_fields=["filename"],
)
index.fit(chunks)

search_call_count = 0


def search(query: str) -> list[dict[str, Any]]:
    global search_call_count

    search_call_count += 1

    return index.search(
        query=query,
        num_results=5,
    )


tools: list[dict[str, Any]] = [
    {
        "type": "function",
        "name": "search",
        "description": "Search the LLM Zoomcamp lesson pages for relevant content.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query",
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    }
]


def run_agent(question: str) -> Any:
    input_messages: list[Any] = [
        {
            "role": "developer",
            "content": INSTRUCTIONS,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    while True:
        response = client.responses.create(
            model=MODEL,
            input=cast(Any, input_messages),
            tools=cast(Any, tools),
        )

        input_messages += response.output

        function_calls = [
            item for item in response.output if item.type == "function_call"
        ]

        if not function_calls:
            return response

        for function_call in function_calls:
            arguments = json.loads(function_call.arguments)

            if function_call.name == "search":
                result = search(arguments["query"])
            else:
                raise ValueError(f"Unknown function: {function_call.name}")

            input_messages.append(
                {
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": json.dumps(result),
                }
            )


def main() -> None:
    response = run_agent(QUESTION)

    print("\nQ6")
    print(response.output_text)
    print(f"Search tool calls: {search_call_count}")


if __name__ == "__main__":
    main()
