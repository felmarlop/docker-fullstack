import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_login_success(public_api_client, user):
    response = public_api_client.post(
        reverse("login"),
        {
            "username": user.username,
            "password": "password123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    assert "access" in response.data
    assert "refresh" in response.data
    assert "user" in response.data

    assert response.data["user"]["id"] == user.id
    assert response.data["user"]["username"] == user.username
    assert response.data["user"]["email"] == user.email


@pytest.mark.django_db
def test_login_invalid_password(public_api_client, user):
    response = public_api_client.post(
        reverse("login"),
        {
            "username": user.username,
            "password": "wrong-password",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    assert "detail" in response.data
