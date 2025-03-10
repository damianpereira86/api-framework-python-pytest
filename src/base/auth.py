import base64
from enum import Enum, auto
from typing import Any, Dict, Optional


class AuthMethod(Enum):
    BEARER = auto()
    BASE64 = auto()
    COOKIE = auto()
    USERNAME_PASSWORD = auto()


class Authenticator:
    """
    Provides various authentication methods using pattern matching to select the appropriate approach.
    """

    @staticmethod
    def authenticate(method: AuthMethod, credentials: Dict[str, Any]) -> Dict[str, Any]:
        match method:
            case AuthMethod.BEARER:
                return Authenticator.authenticate_bearer(credentials.get("token"))
            case AuthMethod.BASE64:
                return Authenticator.authenticate_base64(credentials.get("encoded"))
            case AuthMethod.COOKIE:
                return Authenticator.authenticate_cookie(credentials.get("cookie"))
            case AuthMethod.USERNAME_PASSWORD:
                return Authenticator.authenticate_username_password(
                    credentials.get("username"), credentials.get("password")
                )
            case _:
                raise ValueError("Invalid authentication method provided.")

    @staticmethod
    def authenticate_bearer(token: Optional[str]) -> Dict[str, Any]:
        if not token:
            raise ValueError("Bearer token is required for BEARER authentication.")
        return {"headers": {"Authorization": f"Bearer {token}"}}

    @staticmethod
    def authenticate_base64(encoded: Optional[str]) -> Dict[str, Any]:
        if not encoded:
            raise ValueError("Encoded credentials are required for BASE64 authentication.")
        return {"headers": {"Authorization": f"Basic {encoded}"}}

    @staticmethod
    def authenticate_cookie(cookie: Optional[str]) -> Dict[str, Any]:
        if not cookie:
            raise ValueError("Cookie is required for COOKIE authentication.")
        return {"headers": {"Cookie": cookie}}

    @staticmethod
    def authenticate_username_password(
            username: Optional[str], password: Optional[str]
    ) -> Dict[str, Any]:
        if not username or not password:
            raise ValueError("Username and password are required for USERNAME_PASSWORD authentication.")
        credentials_bytes = f"{username}:{password}".encode("utf-8")
        encoded = base64.b64encode(credentials_bytes).decode("utf-8")
        return {"headers": {"Authorization": f"Basic {encoded}"}}
