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
    Provides authentication methods to select the appropriate approach.
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
        return {"headers": {"Authorization": f"Bearer {token}"}}

    @staticmethod
    def authenticate_base64(encoded: Optional[str]) -> Dict[str, Any]:
        return {"headers": {"Authorization": f"Basic {encoded}"}}

    @staticmethod
    def authenticate_cookie(cookie: Optional[str]) -> Dict[str, Any]:
        return {"headers": {"Cookie": cookie}}

    @staticmethod
    def authenticate_username_password(
        username: Optional[str], password: Optional[str]
    ) -> Dict[str, Any]:
        credentials_bytes = f"{username}:{password}".encode("utf-8")
        encoded = base64.b64encode(credentials_bytes).decode("utf-8")
        return {"headers": {"Authorization": f"Basic {encoded}"}}
