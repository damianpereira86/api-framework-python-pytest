import os
from src.base.ApiClient import ApiClient
from src.base.SessionManager import SessionManager
from src.models.request.CredentialsModel import CredentialsModel
from src.models.responses.Response import Response
from dotenv import load_dotenv
import requests


class ServiceBase:
    """
    Base class for API services. Should be inherited by specific service implementations.

    Example:
        class UserService(ServiceBase):
            def __init__(self):
                super().__init__("users")
    """

    def __init__(self, path: str = ""):
        load_dotenv()
        self.base_url = os.getenv("BASE_URL")
        if not self.base_url:
            raise ValueError("Missing BASE_URL in environment variables.")
        self.url = f"{self.base_url}/{path.strip('/')}"
        self.api = ApiClient()
        self.default_config = {}

    def authenticate(self) -> None:
        username = os.getenv("USER")
        password = os.getenv("PASSWORD")

        if not username or not password:
            raise ValueError("Missing username or password in environment variables.")

        cached_token = SessionManager.get_cached_token(username, password)

        if cached_token:
            self.default_config = {
                "headers": {"Cookie": "token=" + cached_token},
            }
            return

        credentials = CredentialsModel(username=username, password=password)
        response = self.post(f"{self.base_url}/auth", credentials)

        print(response.data)
        SessionManager.store_token(username, password, response.data["token"])

        self.default_config = {
            "headers": {"Cookie": "token=" + response.data["token"]},
        }

    def get(self, url: str, config: dict | None = None) -> Response:
        config = config or self.default_config
        start_time = self._get_current_time()
        response = self.api.client.get(url, **config)
        end_time = self._get_current_time()
        return self._build_response(end_time, start_time, response)

    def post(self, url: str, data: any, config: dict | None = None) -> Response:
        config = config or self.default_config
        start_time = self._get_current_time()
        response = self.api.client.post(url, json=data.model_dump(), **config)
        end_time = self._get_current_time()
        return self._build_response(end_time, start_time, response)

    def put(self, url: str, data: dict, config: dict | None = None) -> Response:
        config = config or self.default_config
        start_time = self._get_current_time()
        response = self.api.client.put(url, json=data, **config)
        end_time = self._get_current_time()
        return self._build_response(end_time, start_time, response)

    def patch(self, url: str, data: dict, config: dict | None = None) -> Response:
        config = config or self.default_config
        start_time = self._get_current_time()
        response = self.api.client.patch(url, json=data, **config)
        end_time = self._get_current_time()
        return self._build_response(end_time, start_time, response)

    def delete(self, url: str, config: dict | None = None) -> Response:
        config = config or self.default_config
        start_time = self._get_current_time()
        response = self.api.client.delete(url, **config)
        end_time = self._get_current_time()
        return self._build_response(end_time, start_time, response)

    def head(self, url: str, config: dict | None = None) -> Response:
        config = config or self.default_config
        start_time = self._get_current_time()
        response = self.api.client.head(url, **config)
        end_time = self._get_current_time()
        return self._build_response(end_time, start_time, response)

    def options(self, url: str, config: dict | None = None) -> Response:
        config = config or self.default_config
        start_time = self._get_current_time()
        response = self.api.client.options(url, **config)
        end_time = self._get_current_time()
        return self._build_response(end_time, start_time, response)

    def _build_response(self, end_time: int, start_time: int, response) -> Response:
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            data = response.text

        return Response(
            status=response.status_code,
            headers=response.headers,
            data=data,
            response_time=end_time - start_time,
        )

    def _get_current_time(self) -> int:
        from time import time

        return int(time() * 1000)
