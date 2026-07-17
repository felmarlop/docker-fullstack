import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_change_password_success(authenticated_api_client, public_api_client, user):
    response = authenticated_api_client.post(
        reverse("change-password"),
        {
            "current_password": "password123",
            "new_password": "new-password123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = public_api_client.post(
        reverse("login"),
        {
            "username": user.username,
            "password": "new-password123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_change_password_invalid_old_password(authenticated_api_client):
    response = authenticated_api_client.post(
        reverse("change-password"),
        {
            "current_password": "wrong-password",
            "new_password": "new-password123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert "current_password" in response.data


@pytest.mark.django_db
def test_change_password_invalid_new_password(authenticated_api_client):
    response = authenticated_api_client.post(
        reverse("change-password"),
        {
            "current_password": "password123",
            "new_password": "1234",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_change_password_same_new_password(authenticated_api_client):
    response = authenticated_api_client.post(
        reverse("change-password"),
        {
            "current_password": "password123",
            "new_password": "password123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert "new_password" in response.data


@pytest.mark.django_db
def test_change_password_requires_authentication(public_api_client):
    response = public_api_client.post(
        reverse("change-password"),
        {
            "current_password": "password123",
            "new_password": "new-password123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
