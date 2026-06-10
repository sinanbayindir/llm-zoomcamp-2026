from dotenv import load_dotenv
from gitsource import GithubRepositoryDataReader,chunk_documents
from minsearch import Index
from openai import OpenAI


QUERY = "How does the agentic loop keep calling the model until it stops?"
MODEL = "gpt-5.4-mini"

load_dotenv()
client = OpenAI()


def load_documents():
    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )

    files = reader.read()
    return [file.parse() for file in files]


def build_index(documents):
    index = Index(
        text_fields=["content"],
        keyword_fields=["filename"],
    )
    index.fit(documents)
    return index


def build_context(results):
    context = ""

    for doc in results:
        context += f"""
filename: {doc["filename"]}
content: {doc["content"]}
""".strip()
        context += "\n\n"

    return context


def build_prompt(query, context):
    return f"""
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT.

Use only the facts from the CONTEXT.
If the CONTEXT doesn't contain the answer, say that you don't know.

QUESTION:
{query}

CONTEXT:
{context}
""".strip()


def ask_llm(prompt):
    return client.responses.create(
        model=MODEL,
        input=prompt,
    )


def main():
    documents = load_documents()

    print("Q1")
    print(f"Number of lesson pages: {len(documents)}")

    index = build_index(documents)

    results = index.search(
        query=QUERY,
        num_results=5,
    )

    print("\nQ2")
    print(f"First result filename: {results[0]['filename']}")

    context = build_context(results)
    prompt = build_prompt(QUERY, context)
    response = ask_llm(prompt)

    print("\nQ3")
    print(response.output_text)

    if response.usage is None:
        raise RuntimeError("No usage information returned by the API response")

    print(f"Input tokens: {response.usage.input_tokens}")


    chunks = chunk_documents(documents, size=2000, step=1000)

    print("\nQ4")
    print(f"Number of chunks: {len(chunks)}")

    chunk_index = build_index(chunks)

    chunk_results = chunk_index.search(

        query=QUERY,

        num_results=5,

    )

    chunk_context = build_context(chunk_results)

    chunk_prompt = build_prompt(QUERY, chunk_context)

    chunk_response = ask_llm(chunk_prompt)

    print("\nQ5")

    print(chunk_response.output_text)

    if chunk_response.usage is None:

        raise RuntimeError("No usage information returned by the API response")

    chunk_input_tokens = chunk_response.usage.input_tokens

    print(f"Chunked input tokens: {chunk_input_tokens}")

    print(f"Token reduction ratio: {response.usage.input_tokens / chunk_input_tokens:.2f}x")

if __name__ == "__main__":
    main()
