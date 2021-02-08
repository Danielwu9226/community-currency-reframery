from locust import HttpUser, task, between
import string
import random

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def register(self):
        email = ''.join((''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),'@email.com'))
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print({"email": email, "password": password})
        print(self.client.post('/register/', json={"email": email, "password": password}).content)
