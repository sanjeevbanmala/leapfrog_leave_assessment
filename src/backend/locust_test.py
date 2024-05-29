import os
import sys
from locust import HttpUser, task, between


# Import the Flask app
from main import app


class MyUser(HttpUser):
    wait_time = between(1, 3)  # Time between consecutive requests

    @task
    def get_leave_info(self):
        # Send a GET request to /leave_info endpoint
        self.client.get("/leave_info")
