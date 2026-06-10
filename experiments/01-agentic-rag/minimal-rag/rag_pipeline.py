from rag import rag


if __name__ == "__main__":
    question = "Can I still join the course?"
    course_name = "llm-zoomcamp"

    answer = rag(question, course_name)
    print(answer)
