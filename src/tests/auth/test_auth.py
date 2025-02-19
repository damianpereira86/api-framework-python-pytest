import os
import pytest
from src.models import AuthService, CredentialsModel


@pytest.fixture
def auth_service():
    return AuthService()


def test_sign_in_with_valid_credentials(auth_service):
    credentials = CredentialsModel(
        username=os.getenv("USER"), password=os.getenv("PASSWORD")
    )
    response = auth_service.signIn(credentials)
    assert response.status == 200


def test_sign_in_with_wrong_username(auth_service):
    credentials = CredentialsModel(
        username="wrong_username", password=os.getenv("PASSWORD")
    )
    response = auth_service.signIn(credentials)
    assert response.status == 200
    assert response.data["reason"] == "Bad credentials"


def test_sign_in_with_wrong_password(auth_service):
    credentials = CredentialsModel(
        username=os.getenv("USER"), password="wrong_password"
    )
    response = auth_service.signIn(credentials)
    assert response.status == 200
    assert response.data["reason"] == "Bad credentials"
