import requests


class ApiClientBase:
    def __init__(self):
        self.client = requests.Session()
        self.client.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
