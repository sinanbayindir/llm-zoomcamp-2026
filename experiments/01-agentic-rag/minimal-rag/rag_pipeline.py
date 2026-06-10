from rag import rag


if __name__ == "__main__":
    question = "When does the course start?"
    course_name = "data-engineering-zoomcamp"

    answer = rag(question, course_name)
    print(answer)
