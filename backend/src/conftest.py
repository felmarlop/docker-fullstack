import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from app.authentication.models import User


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username="fmartin",
        email="fmartin@test.com",
        phone="+34600111222",
        password="password123",
    )


@pytest.fixture
def user_no_password() -> User:
    user = User.objects.create_user(
        username="fmartin",
        email="fmartin@test.com",
        phone="+34600111222",
    )
    user.set_unusable_password()
    user.save(update_fields=["password"])
    return user


@pytest.fixture
def public_api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticated_api_client(user: User) -> APIClient:
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client


@pytest.fixture
def authenticated_api_client_no_password(user_no_password: User) -> APIClient:
    client = APIClient()
    refresh = RefreshToken.for_user(user_no_password)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client
