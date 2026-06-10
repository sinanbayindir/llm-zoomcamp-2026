import requests

COURSES_URL = "https://datatalks.club/faq/json/courses.json"

URL_PREFIX = "https://datatalks.club/faq"

response = requests.get(COURSES_URL)

response.raise_for_status()

courses = response.json()

print(type(courses))

print(len(courses))

print(courses[0])

course_url = f"{URL_PREFIX}{courses[0]['path']}"

course_response = requests.get(course_url)

course_response.raise_for_status()

documents = course_response.json()

print(type(documents))

print(len(documents))

print(documents[0].keys())

print(documents[0])
