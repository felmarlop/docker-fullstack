from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
import stripe
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from app.authentication.models import User
from app.subscription.models import StripeCustomer
from app.subscription.stripe import api as stripe_api


@pytest.fixture
def user() -> User:
    customers = stripe_api.client.customers.list(params={"limit": 1})
    if not customers.data:
        raise RuntimeError("At least one Stripe customer is required for tests.")

    u = User.objects.create_user(
        username="fmartin",
        email="fmartin@test.com",
        phone="+34600111222",
        password="password123",
    )

    StripeCustomer.objects.create(
        user=u,
        stripe_customer_id=customers.data[0].id,
    )

    return u


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


@pytest.fixture
def stripe_payment_intent_mock() -> Generator[MagicMock]:
    payment_intent = stripe.PaymentIntent.construct_from(
        {
            "id": "test_intent",
            "amount": 999,
            "currency": "eur",
            "client_secret": "test_intent_secret",
        },
        "sk_test",
    )

    with patch.object(
        stripe_api,
        "create_payment_intent",
        return_value=payment_intent,
    ) as mock:
        yield mock


@pytest.fixture
def stripe_cancel_payment_intent_mock() -> Generator[MagicMock]:
    with patch.object(
        stripe_api,
        "cancel_payment_intent",
        return_value=None,
    ) as mock:
        yield mock
