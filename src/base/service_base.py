import os
from http import HTTPMethod
from time import time
from typing import Any, Dict, Optional, Type, TypeVar, List, get_args
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from requests import Session

from src.base.auth import Authenticator, AuthMethod
from src.base.cookie_store import CookieHeaderStore
from src.base.session_manager import SessionManager
from src.models.requests.credentials.credentials_model import CredentialsModel
from src.models.responses.auth.auth_response import AuthResponse
from src.models.responses.base.response import Response

T = TypeVar("T", bound=BaseModel | List[BaseModel])


class ServiceBase(Session):
    """
    Base class for API services. Should be inherited by specific service implementations.

    Example:
        class UserService(ServiceBase):
            def __init__(self):
                super().__init__("users", base_url="https://api.example.com")
    """

    def __init__(
        self, path: str = "", base_url: str = "", store_name: str = None
    ) -> None:
        super().__init__()
        load_dotenv(override=True)

        self.base_url = base_url or os.getenv("BASE_URL")
        if not self.base_url:
            raise ValueError("A valid base_url must be provided.")
        self.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        self.url = f"{self.base_url}/{path.strip('/')}"
        self.default_config: Dict[str, Any] = {}

        if not store_name:
            store_name = os.urandom(15).hex()
        self.store = CookieHeaderStore(store_name)
        self.headers.update(self.store.headers)
        self.cookies.update(self.store.cookies)

    def get(
        self, url: str, response_model: Type[T] = None, **kwargs: Any
    ) -> Response[T]:
        return self._request(
            HTTPMethod.GET, url, response_model=response_model, **kwargs
        )

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        response_model: Type[T] = None,
        **kwargs: Any,
    ) -> Response[T]:
        return self._request(
            HTTPMethod.POST, url, data, response_model=response_model, **kwargs
        )

    def put(
        self,
        url: str,
        data: Optional[Any] = None,
        response_model: Type[T] = None,
        **kwargs: Any,
    ) -> Response[T]:
        return self._request(
            HTTPMethod.PUT, url, data, response_model=response_model, **kwargs
        )

    def patch(
        self,
        url: str,
        data: Optional[Any] = None,
        response_model: Type[T] = None,
        **kwargs: Any,
    ) -> Response[T]:
        return self._request(
            HTTPMethod.PATCH, url, data, response_model=response_model, **kwargs
        )

    def delete(
        self, url: str, response_model: Type[T] = None, **kwargs: Any
    ) -> Response[T]:
        return self._request(
            HTTPMethod.DELETE, url, response_model=response_model, **kwargs
        )

    def options(
        self, url: str, response_model: Type[T] = None, **kwargs: Any
    ) -> Response[T]:
        return self._request(
            HTTPMethod.OPTIONS, url, response_model=response_model, **kwargs
        )

    def head(
        self, url: str, response_model: Type[T] = None, **kwargs: Any
    ) -> Response[T]:
        return self._request(
            HTTPMethod.HEAD, url, response_model=response_model, **kwargs
        )

    def trace(
        self, url: str, response_model: Type[T] = None, **kwargs: Any
    ) -> Response[T]:
        return self._request(
            HTTPMethod.TRACE, url, response_model=response_model, **kwargs
        )

    def connect(
        self, url: str, response_model: Type[T] = None, **kwargs: Any
    ) -> Response[T]:
        return self._request(
            HTTPMethod.CONNECT, url, response_model=response_model, **kwargs
        )

    def _request(
        self,
        method: str,
        url: str,
        data: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None,
        response_model: Type[T] = None,
        **kwargs: Any,
    ) -> Response[T]:
        config = config or self.default_config
        start_time = int(time() * 1000)

        has_model_dump = data and hasattr(data, "model_dump")
        json_payload = data.model_dump(exclude_none=True) if has_model_dump else data

        response = getattr(super(), method.lower())(
            url, json=json_payload, **config, **kwargs
        )
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

    def authenticate(
        self,
        auth_method: AuthMethod = AuthMethod.USERNAME_PASSWORD,
        credentials: Dict[str, Any] = None,
    ) -> None:
        """
        Uses the specified authentication method to generate the auth headers.

        Args:
            auth_method (AuthMethod): The authentication method to use.
            credentials (Dict[str, Any]): A dictionary of credentials.
                For BEARER: expects {"token": str}.
                For BASE64: expects {"encoded": str}.
                For COOKIE: expects {"cookie": str}.
                For USERNAME_PASSWORD: expects {"username": str, "password": str}.
        """
        if not credentials:
            credentials = {
                "username": os.getenv("USERNAME"),
                "password": os.getenv("PASSWORD"),
            }

        auth_config = Authenticator.authenticate(auth_method, credentials)

        if auth_method != AuthMethod.USERNAME_PASSWORD:
            self.default_config = auth_config
            return

        username = credentials.get("username")
        password = credentials.get("password")
        cached_token = SessionManager.get_cached_token(username, password)
        if cached_token:
            self.store.headers["Cookie"] = f"token={cached_token}"
            self.headers.update(self.store.headers)
            return

        credentials_req = CredentialsModel(username=username, password=password)
        response = self.post(f"{self.base_url}/auth", data=credentials_req)

        raw_data = response.data
        auth_response = AuthResponse.model_validate(raw_data)
        SessionManager.store_token(username, password, auth_response.token)
        self.store.headers["Cookie"] = f"token={auth_response.token}"
        self.headers.update(self.store.headers)
