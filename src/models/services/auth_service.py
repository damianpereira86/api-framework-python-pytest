from src.base.service_base import ServiceBase
from src.models.requests.credentials.credentials_model import CredentialsModel


class AuthService(ServiceBase):
    def __init__(self, store_name: str = None):
        super().__init__("auth", store_name=store_name)

    def sign_in(self, credentials: CredentialsModel):
        return self.post(self.url, credentials)
