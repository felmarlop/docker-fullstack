import pytest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APIClient

from app.authentication.models import User

COMMON_PASSWORD = "12345678"
VALID_PASSWORD = "fmartinStrong123"
SECOND_VALID_PASSWORD = "fmartinStrongAgain123"


@pytest.mark.django_db
def test_forgot_password_valid_and_invalid_email(
    public_api_client: APIClient,
    user: User,  # noqa: ARG001
) -> None:
    response = public_api_client.post(
        reverse("forgot-password"),
        {"email": "f_martin@test.com"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = public_api_client.post(
        reverse("forgot-password"),
        {"email": "fmartin@test.com"},
        format="json",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data


@pytest.mark.django_db
def test_reset_password_success(public_api_client: APIClient, user: User) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)

    response = public_api_client.post(
        reverse("reset-password"),
        {"uid": uid, "token": token, "new_password": VALID_PASSWORD},
        format="json",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    user.refresh_from_db()
    assert user.check_password(VALID_PASSWORD)


@pytest.mark.django_db
def test_reset_password_too_common(public_api_client: APIClient, user: User) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)

    response = public_api_client.post(
        reverse("reset-password"),
        {"uid": uid, "token": token, "new_password": COMMON_PASSWORD},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "new_password" in response.data
    assert "too common" in response.data["new_password"][0].lower()


@pytest.mark.django_db
def test_reset_password_invalid_uid(public_api_client: APIClient, user: User) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)
    uid = f"{uid}invalid"

    response = public_api_client.post(
        reverse("reset-password"),
        {"uid": uid, "token": token, "new_password": VALID_PASSWORD},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "uid" in response.data


@pytest.mark.django_db
def test_reset_password_invalid_token(public_api_client: APIClient, user: User) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)
    token = f"{token}invalid"

    response = public_api_client.post(
        reverse("reset-password"),
        {"uid": uid, "token": token, "new_password": VALID_PASSWORD},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "token" in response.data


@pytest.mark.django_db
def test_reset_password_token_cannot_be_reused(
    public_api_client: APIClient, user: User
) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)

    response = public_api_client.post(
        reverse("reset-password"),
        {"uid": uid, "token": token, "new_password": VALID_PASSWORD},
        format="json",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    user.refresh_from_db()
    assert user.check_password(VALID_PASSWORD)

    response = public_api_client.post(
        reverse("reset-password"),
        {"uid": uid, "token": token, "new_password": SECOND_VALID_PASSWORD},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "token" in response.data
