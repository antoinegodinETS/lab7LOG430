from locust import HttpUser, task, between

class InterfaceUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def access_index(self):
        self.client.get("/")

    @task
    def access_performances(self):
        self.client.get("/performances")

    @task
    def access_rapport(self):
        self.client.get("/rapport")
