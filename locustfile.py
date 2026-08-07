from locust import HttpUser, task, between


class JobPortalUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        response = self.client.post(
            "/accounts/login/",
            json={
                "email": "recruiter1@test.com",
                "password": "123456789"
            }
        )

        print("Login Status:", response.status_code)
        print(response.text)

        if response.status_code != 200:
            raise Exception("Login failed")

        data = response.json()

        token = data["data"]["access"]   # <-- your login response nests the token inside "data"

        self.client.headers.update({
            "Authorization": f"Bearer {token}"
        })

    @task
    def analytics(self):
        self.client.get("/analytics/dashboard/")

    @task
    def report(self):
        self.client.get("/ai/report/1/")