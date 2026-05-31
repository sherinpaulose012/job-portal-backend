import requests

data = {
    "title": "Backend Learning",
    "body": "Learning APIs",
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=data
)

print(response.json())
print(response.status_code)