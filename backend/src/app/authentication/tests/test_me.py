import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.authentication.models import User


@pytest.mark.django_db
def test_me(authenticated_api_client: APIClient, user: User) -> None:
    response = authenticated_api_client.get(reverse("users-me"))

    assert response.status_code == status.HTTP_200_OK

    assert response.data["id"] == user.id
    assert response.data["username"] == user.username
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_me_requires_authentication(public_api_client: APIClient) -> None:
    response = public_api_client.get(reverse("users-me"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
