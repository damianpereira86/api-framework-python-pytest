import os
from time import time
from typing import Any, Dict, Optional, Type, TypeVar, List, get_args
import requests
from dotenv import load_dotenv
from pydantic import BaseModel

from src.base.api_client import api_client_instance
from src.base.auth import Authenticator, AuthMethod
from src.base.session_manager import SessionManager
from src.models.requests.credentials.credentials_model import CredentialsModel
from src.models.responses.auth.auth_response import AuthResponse
from src.models.responses.base.response import Response
from src.models.shared.http_methods import Method

T = TypeVar("T", bound=BaseModel | List[BaseModel])


class ServiceBase:
    """
    Base class for API services. Should be inherited by specific service implementations.

    Example:
        class UserService(ServiceBase):
            def __init__(self):
                super().__init__("users", base_url="https://api.example.com")
    """

    def __init__(self, path: str = "", base_url: str = "") -> None:
        load_dotenv(override=True)
        self.base_url = base_url or os.getenv("BASE_URL")
        if not self.base_url:
            raise ValueError("A valid base_url must be provided.")
        self.url = f"{self.base_url}/{path.strip('/')}"
        self.api = api_client_instance
        self.default_config: Dict[str, Any] = {}

    def authenticate(
            self,
            auth_method: AuthMethod = AuthMethod.USERNAME_PASSWORD,
            credentials: Dict[str, Any] = None
    ) -> None:
        """
        Uses the specified authentication method to generate a configuration with the proper HTTP headers.

        Args:
            auth_method (AuthMethod): The authentication method to use.
            credentials (Dict[str, Any]): A dictionary of credentials.
                For BEARER: expects {"token": str}.
                For BASE64: expects {"encoded": str}.
                For COOKIE: expects {"cookie": str}.
                For USERNAME_PASSWORD: expects {"username": str, "password": str}.
        """
        if not credentials:
            credentials = {"username": os.getenv("USERNAME"), "password": os.getenv("PASSWORD")}

        auth_config = Authenticator.authenticate(auth_method, credentials)

        if auth_method != AuthMethod.USERNAME_PASSWORD:
            self.default_config = auth_config
            return

        username = credentials.get("username")
        password = credentials.get("password")
        cached_token = SessionManager.get_cached_token(username, password)
        if cached_token:
            self.default_config = {"headers": {"Cookie": f"token={cached_token}"}}
            return

        credentials_req = CredentialsModel(username=username, password=password)
        response = self.api.client.post(f"{self.base_url}/auth", json=credentials_req.__dict__)

        raw_data = response.json()
        auth_response = AuthResponse.model_validate(raw_data)
        SessionManager.store_token(credentials["username"], credentials["password"], auth_response.token)
        self.default_config = {"headers": {"Cookie": f"token={auth_response.token}"}}

    def request(
            self,
            method: Method,
            url: str,
            data: Optional[Any] = None,
            config: Optional[Dict[str, Any]] = None,
            response_model: Type[T] = None,
    ) -> Response[T]:
        config = config or self.default_config
        start_time = int(time() * 1000)

        json_payload = data.model_dump(exclude_none=True) if data and hasattr(data, "model_dump") else None

        response = getattr(self.api.client, method.value)(url, json=json_payload, **config)
        end_time = int(time() * 1000)

        try:
            raw_data = response.json()
            if response_model and isinstance(raw_data, list):
                model = get_args(response_model)[0]
                parsed_data = [model.model_validate(item) for item in raw_data]
            elif response_model:
                parsed_data = response_model.model_validate(raw_data)
            else:
                parsed_data = raw_data
        except (requests.exceptions.JSONDecodeError, ValueError):
            parsed_data = response.text

        return Response(
            status=response.status_code,
            headers=response.headers,
            data=parsed_data,
            response_time=end_time - start_time,
        )
