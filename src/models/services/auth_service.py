from src.base.service_base import ServiceBase
from src.models.requests.credentials.credentials_model import CredentialsModel
from src.models.shared.http_methods import Method


class AuthService(ServiceBase):
    def __init__(self):
        super().__init__("auth")

    def sign_in(self, credentials: CredentialsModel):
        return self.request(method=Method.Post, url=self.url, data=credentials)
