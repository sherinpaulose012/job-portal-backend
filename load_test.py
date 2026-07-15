import threading
import requests

URL = "http://127.0.0.1:8000/applications/recommendations/"

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgzNzQ5MzI3LCJpYXQiOjE3ODM3NDg0MjcsImp0aSI6Ijc0MGQyNWIzZWVkODQxZmJiMmY3ODYzZDBhZmMyZTFlIiwidXNlcl9pZCI6IjExIn0.T89zWo81fw8apsNFHYkjhMnVu21-gIeBzDmNXNNtQYc"


def send_request():

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(URL, headers=headers)

    print(response.status_code)


threads = []

for i in range(20):

    t = threading.Thread(
        target=send_request
    )

    threads.append(t)

    t.start()

for t in threads:
    t.join()

print("Load Test Completed")