import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_logout_success(authenticated_api_client, user):
    refresh = str(RefreshToken.for_user(user))
    response = authenticated_api_client.post(
        reverse("logout"),
        {
            "refresh": refresh,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_logout_invalid_refresh(authenticated_api_client):
    response = authenticated_api_client.post(
        reverse("logout"),
        {
            "refresh": "invalid-token",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert "refresh" in response.data


@pytest.mark.django_db
def test_logout_requires_authentication(public_api_client, user):
    refresh = str(RefreshToken.for_user(user))
    response = public_api_client.post(
        reverse("logout"),
        {
            "refresh": refresh,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_logout_blacklists_refresh_token(
    authenticated_api_client, public_api_client, user
):
    refresh = str(RefreshToken.for_user(user))
    response = authenticated_api_client.post(
        reverse("logout"),
        {
            "refresh": refresh,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Use the public client because the access token may already be expired
    response = public_api_client.post(
        reverse("token-refresh"),
        {
            "refresh": refresh,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
