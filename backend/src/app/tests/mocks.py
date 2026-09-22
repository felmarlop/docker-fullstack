from collections.abc import Callable, Generator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import stripe

from app.subscription import services
from app.subscription.models.choices import StripePaymentStatus
from app.subscription.stripe import api as stripe_api


@pytest.fixture
def get_stripe_customer_mock() -> Generator[MagicMock]:
    customer = stripe.Customer.construct_from(
        {
            "id": "cus_test",
        },
        "sk_test",
    )
    with patch.object(
        stripe_api.client.customers,
        "retrieve",
        return_value=customer,
    ) as mock:
        yield mock


@pytest.fixture
def get_stripe_price_mock() -> Generator[MagicMock]:
    price = stripe.Price.construct_from(
        {
            "id": "price_test",
            "active": True,
            "unit_amount": 999,
            "currency": "eur",
            "product": {
                "id": "prod_test",
                "name": "Test Product",
            },
        },
        "sk_test",
    )

    with patch.object(
        stripe_api.client.prices,
        "retrieve",
        return_value=price,
    ) as mock:
        yield mock


@pytest.fixture
def stripe_payment_intent_mock(
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[..., stripe.PaymentIntent]:
    def _build(
        *,
        id: str = "test_intent",
        status: str = StripePaymentStatus.REQUIRES_PAYMENT,
    ) -> stripe.PaymentIntent:
        payment_intent = stripe.PaymentIntent.construct_from(
            {
                "id": id,
                "amount": 999,
                "currency": "eur",
                "client_secret": f"{id}_secret",
                "status": status,
            },
            "sk_test",
        )

        monkeypatch.setattr(
            stripe_api,
            "create_payment_intent",
            lambda *args, **kwargs: payment_intent,  # noqa
        )

        return payment_intent

    return _build


@pytest.fixture
def get_payment_intent_mock(
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[..., stripe.PaymentIntent]:
    def _build(
        *,
        id: str = "test_intent",
        status: str = StripePaymentStatus.REQUIRES_PAYMENT,
    ) -> stripe.PaymentIntent:
        payment_intent = stripe.PaymentIntent.construct_from(
            {
                "id": id,
                "amount": 999,
                "currency": "eur",
                "status": status,
                "client_secret": "test_intent_secret",
            },
            "sk_test",
        )

        monkeypatch.setattr(
            stripe_api,
            "get_payment_intent",
            lambda *args, **kwargs: payment_intent,  # noqa
        )

        return payment_intent

    return _build


@pytest.fixture
def stripe_cancel_payment_intent_mock() -> Generator[MagicMock]:
    payment_intent = stripe.PaymentIntent.construct_from(
        {
            "id": "test_intent",
            "amount": 999,
            "currency": "eur",
            "status": StripePaymentStatus.CANCELED,
            "client_secret": "test_intent_secret",
        },
        "sk_test",
    )
    with patch.object(
        stripe_api,
        "cancel_payment_intent",
        return_value=payment_intent,
    ) as mock:
        yield mock


@pytest.fixture
def stripe_webhook_event(
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[..., stripe.Event]:
    def _build(
        *,
        event_type: str,
        payment_intent_id: str,
        payment_intent_status: str,
    ) -> stripe.Event:
        payment_intent = MagicMock()
        payment_intent.id = payment_intent_id
        payment_intent.status = payment_intent_status

        event = MagicMock()
        event.id = "evt_test"
        event.type = event_type
        event.data.object = payment_intent

        monkeypatch.setattr(
            stripe.Webhook,
            "construct_event",
            lambda *args, **kwargs: event,  # noqa
        )

        return event

    return _build


@pytest.fixture
def sync_subscription_status_mock(
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[..., None]:
    _sync = services.sync_subscription_status

    def _sync_error(*args: Any, **kwargs: Any) -> None:  # noqa: ARG001
        raise RuntimeError("Temporary error")

    def _build(*, raise_error: bool = False) -> None:
        monkeypatch.setattr(
            services,
            "sync_subscription_status",
            _sync_error if raise_error else _sync,
        )

    return _build
