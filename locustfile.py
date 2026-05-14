from locust import HttpUser, task, between
class SenseMindUser(HttpUser):
    wait_time = between(1, 2)
    @task(3)
    def view_status(self):
        self.client.get("/api/v1/status/current/1")
    @task(1)
    def post_data(self):
        self.client.post("/api/v1/data/raw", json={
            "device_id": 1,
            "hrv_raw": 65.5,
            "gsr_raw": 1.2
        })
