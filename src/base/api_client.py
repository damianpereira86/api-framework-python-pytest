import requests


class ApiClient:
    def __init__(self):
        self.client = requests.Session()
        self.client.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )


api_client_instance = ApiClient()
