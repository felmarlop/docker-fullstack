import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APIClient

from app.authentication.models import User

VALID_PASSWORD = "fmartinStrong123"


@pytest.mark.django_db
def test_register_success(public_api_client: APIClient) -> None:
    response = public_api_client.post(
        reverse("register"),
        {
            "username": "fmartin",
            "email": "fmartin@test.com",
            "password": VALID_PASSWORD,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(username="fmartin")

    assert user.email == "fmartin@test.com"
    assert not user.is_active
    assert user.phone is None
    assert user.check_password(VALID_PASSWORD)


@pytest.mark.django_db
def test_register_username_normalized(public_api_client: APIClient) -> None:
    response = public_api_client.post(
        reverse("register"),
        {
            "username": "fMarTin",
            "email": "fmartin@test.com",
            "password": VALID_PASSWORD,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(username="fmartin")

    assert user.username == "fmartin"
    assert user.email == "fmartin@test.com"


@pytest.mark.django_db
def test_register_no_username(public_api_client: APIClient) -> None:
    response = public_api_client.post(
        reverse("register"),
        {
            "username": "",
            "email": "fmartin.73@test.com",
            "password": VALID_PASSWORD,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(username="fmartin.73")

    assert user.email == "fmartin.73@test.com"
    assert not user.is_active


@pytest.mark.django_db
def test_register_with_phone(public_api_client: APIClient) -> None:
    response = public_api_client.post(
        reverse("register"),
        {
            "username": "fmartin",
            "email": "fmartin@test.com",
            "password": VALID_PASSWORD,
            "phone": "+34600111222",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(username="fmartin")

    assert str(user.phone) == "+34600111222"
    assert not user.is_phone_verified


@pytest.mark.django_db
def test_register_phone_already_exists(public_api_client: APIClient) -> None:
    User.objects.create_user(
        username="existing",
        email="existing@test.com",
        password=VALID_PASSWORD,
        phone="+34600111222",
    )

    response = public_api_client.post(
        reverse("register"),
        {
            "username": "fmartin",
            "email": "fmartin@test.com",
            "password": VALID_PASSWORD,
            "phone": "+34600111222",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "phone" in response.data


@pytest.mark.django_db
def test_register_reserved_username(public_api_client: APIClient) -> None:
    response = public_api_client.post(
        reverse("register"),
        {
            "username": "admin",
            "email": "admin@test.com",
            "password": VALID_PASSWORD,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_activate_account_success(
    public_api_client: APIClient,
    user: User,
) -> None:
    user.is_active = False
    user.save(update_fields=["is_active"])

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    response = public_api_client.get(
        reverse(
            "activate-account",
            kwargs={
                "uidb64": uid,
                "token": token,
            },
        )
    )

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()

    assert user.is_active


@pytest.mark.django_db
def test_activate_account_token_cannot_be_reused(
    public_api_client: APIClient,
    user: User,
) -> None:
    user.is_active = False
    user.save(update_fields=["is_active"])

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    response = public_api_client.get(
        reverse(
            "activate-account",
            kwargs={
                "uidb64": uid,
                "token": token,
            },
        )
    )

    assert response.status_code == status.HTTP_200_OK

    response = public_api_client.get(
        reverse(
            "activate-account",
            kwargs={
                "uidb64": uid,
                "token": token,
            },
        )
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "user" in response.data


@pytest.mark.django_db
def test_activate_account_invalid_token(
    public_api_client: APIClient,
    user: User,
) -> None:
    user.is_active = False
    user.save(update_fields=["is_active"])

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = f"{default_token_generator.make_token(user)}invalid"

    response = public_api_client.get(
        reverse(
            "activate-account",
            kwargs={
                "uidb64": uid,
                "token": token,
            },
        )
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "token" in response.data
