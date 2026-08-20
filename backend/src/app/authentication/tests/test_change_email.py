import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.authentication.models import User
from app.authentication.tokens import generate_email_verification_token


@pytest.mark.django_db
def test_change_email_success(
    authenticated_api_client: APIClient,
    user: User,
) -> None:
    response = authenticated_api_client.post(
        reverse("change-email"),
        {
            "email": "new@example.com",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username

    user.refresh_from_db()

    assert user.email != "new@example.com"
    assert user.pending_email == "new@example.com"


@pytest.mark.django_db
def test_change_email_same_email(
    authenticated_api_client: APIClient,
    user: User,
) -> None:
    response = authenticated_api_client.post(
        reverse("change-email"),
        {
            "email": user.email,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_change_email_existing_email(
    authenticated_api_client: APIClient,
) -> None:
    User.objects.create_user(
        username="another",
        email="another@example.com",
        password="password123",
    )

    response = authenticated_api_client.post(
        reverse("change-email"),
        {
            "email": "another@example.com",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_change_email_invalid_email(
    authenticated_api_client: APIClient,
) -> None:
    response = authenticated_api_client.post(
        reverse("change-email"),
        {
            "email": "not-an-email",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_change_email_requires_authentication(
    public_api_client: APIClient,
) -> None:
    response = public_api_client.post(
        reverse("change-email"),
        {
            "email": "new@example.com",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data


@pytest.mark.django_db
def test_change_email_replaces_pending_email(
    authenticated_api_client: APIClient,
    user: User,
) -> None:
    user.pending_email = "old@example.com"
    user.save(update_fields=["pending_email"])

    response = authenticated_api_client.post(
        reverse("change-email"),
        {
            "email": "new@example.com",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username

    user.refresh_from_db()

    assert user.pending_email == "new@example.com"


@pytest.mark.django_db
def test_change_email_existing_pending_email(
    authenticated_api_client: APIClient,
) -> None:
    User.objects.create_user(
        username="another",
        email="another@example.com",
        pending_email="pending@example.com",
        password="password123",
    )

    response = authenticated_api_client.post(
        reverse("change-email"),
        {
            "email": "pending@example.com",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_change_email_strips_email(
    authenticated_api_client: APIClient,
    user: User,
) -> None:
    response = authenticated_api_client.post(
        reverse("change-email"),
        {
            "email": "  new@example.com  ",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()

    assert user.pending_email == "new@example.com"


@pytest.mark.django_db
def test_verify_email_success(
    public_api_client: APIClient,
    user: User,
) -> None:
    user.pending_email = "new@example.com"
    user.save(update_fields=["pending_email"])

    uidb64, token = generate_email_verification_token(user)

    response = public_api_client.get(
        reverse(
            "verify-email",
            kwargs={
                "uidb64": uidb64,
                "token": token,
            },
        )
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username

    user.refresh_from_db()

    assert user.email == "new@example.com"
    assert user.pending_email is None

    # Not possible to verify twice
    response = public_api_client.get(
        reverse(
            "verify-email",
            kwargs={
                "uidb64": uidb64,
                "token": token,
            },
        )
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_verify_email_invalid_link(
    public_api_client: APIClient,
    user: User,
) -> None:
    user.pending_email = "new@example.com"
    user.save(update_fields=["pending_email"])

    uidb64, _ = generate_email_verification_token(user)

    response = public_api_client.get(
        reverse(
            "verify-email",
            kwargs={
                "uidb64": uidb64,
                "token": "invalid-token",
            },
        )
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = public_api_client.get(
        reverse(
            "verify-email",
            kwargs={
                "uidb64": "invalid",
                "token": "whatever",
            },
        )
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_verify_email_without_pending_email(
    public_api_client: APIClient,
    user: User,
) -> None:
    uidb64, token = generate_email_verification_token(user)

    response = public_api_client.get(
        reverse(
            "verify-email",
            kwargs={
                "uidb64": uidb64,
                "token": token,
            },
        )
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
