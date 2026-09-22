from collections.abc import Callable

import pytest
import stripe
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.authentication.models import User
from app.subscription.models import Payment, Subscription
from app.subscription.models.choices import (
    PaymentStatus,
    StripePaymentStatus,
    SubscriptionStatus,
)


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_webhook_payment_pending_succeeded(
    authenticated_api_client: APIClient,
    user: User,
    stripe_payment_intent_mock: Callable[..., stripe.Event],
    stripe_webhook_event: Callable[..., stripe.Event],
) -> None:
    stripe_payment_intent_mock()

    response = authenticated_api_client.post(
        reverse("create-subscription"),
        {
            "plan": "plus-lifetime",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    subscription_obj = response.data["subscription"]
    assert subscription_obj["username"] == user.username
    assert subscription_obj["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(subscription_id=subscription_obj["id"])
    assert payments.count() == 1

    payment = payments.first()
    assert payment is not None
    assert payment.status == PaymentStatus.PENDING

    subscription = Subscription.objects.get(pk=payment.subscription_id)
    assert subscription.status == SubscriptionStatus.PENDING

    stripe_webhook_event(
        event_type="payment_intent.succeeded",
        payment_intent_id=payment.stripe_payment_intent_id,
        payment_intent_status=PaymentStatus.SUCCEEDED,
    )

    response = authenticated_api_client.post(
        "/api/subscriptions/stripe/webhook/",
        data=b"{}",
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test-signature",
    )
    assert response.status_code == status.HTTP_200_OK

    payment.refresh_from_db()
    subscription.refresh_from_db()

    assert payment.status == PaymentStatus.SUCCEEDED
    assert subscription.status == SubscriptionStatus.ACTIVE


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_webhook_payment_processing_canceled(
    authenticated_api_client: APIClient,
    user: User,
    stripe_payment_intent_mock: Callable[..., stripe.Event],
    stripe_webhook_event: Callable[..., stripe.Event],
) -> None:
    stripe_payment_intent_mock()

    response = authenticated_api_client.post(
        reverse("create-subscription"),
        {
            "plan": "plus-lifetime",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    subscription_obj = response.data["subscription"]
    assert subscription_obj["username"] == user.username
    assert subscription_obj["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(subscription_id=subscription_obj["id"])
    assert payments.count() == 1

    payment = payments.first()
    assert payment is not None
    assert payment.status == PaymentStatus.PENDING

    subscription = Subscription.objects.get(pk=payment.subscription_id)
    assert subscription.status == SubscriptionStatus.PENDING

    stripe_webhook_event(
        event_type="payment_intent.succeeded",
        payment_intent_id=payment.stripe_payment_intent_id,
        payment_intent_status=PaymentStatus.CANCELED,
    )

    response = authenticated_api_client.post(
        "/api/subscriptions/stripe/webhook/",
        data=b"{}",
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test-signature",
    )
    assert response.status_code == status.HTTP_200_OK

    payment.refresh_from_db()
    subscription.refresh_from_db()

    assert payment.status == PaymentStatus.CANCELED
    assert subscription.status == SubscriptionStatus.CANCELED


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_webhook_payment_processing_succeeded(
    authenticated_api_client: APIClient,
    user: User,
    stripe_payment_intent_mock: Callable[..., stripe.Event],
    stripe_webhook_event: Callable[..., stripe.Event],
) -> None:
    stripe_payment_intent_mock()

    response = authenticated_api_client.post(
        reverse("create-subscription"),
        {
            "plan": "plus-lifetime",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    subscription_obj = response.data["subscription"]
    assert subscription_obj["username"] == user.username
    assert subscription_obj["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(subscription_id=subscription_obj["id"])
    assert payments.count() == 1

    payment = payments.first()
    assert payment is not None
    assert payment.status == PaymentStatus.PENDING

    subscription = Subscription.objects.get(pk=payment.subscription_id)
    assert subscription.status == SubscriptionStatus.PENDING

    stripe_webhook_event(
        event_type="payment_intent.succeeded",
        payment_intent_id=payment.stripe_payment_intent_id,
        payment_intent_status=PaymentStatus.SUCCEEDED,
    )

    response = authenticated_api_client.post(
        "/api/subscriptions/stripe/webhook/",
        data=b"{}",
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test-signature",
    )
    assert response.status_code == status.HTTP_200_OK

    payment.refresh_from_db()
    subscription.refresh_from_db()

    assert payment.status == PaymentStatus.SUCCEEDED
    assert subscription.status == SubscriptionStatus.ACTIVE


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_webhook_cancel_old_active_subscription(
    authenticated_api_client: APIClient,
    user: User,
    stripe_webhook_event: Callable[..., stripe.Event],
    stripe_payment_intent_mock: Callable[..., stripe.Event],
    get_payment_intent_mock: Callable[..., stripe.Event],
) -> None:
    stripe_payment_intent_mock()
    get_payment_intent_mock(status=StripePaymentStatus.SUCCEEDED)

    response = authenticated_api_client.post(
        reverse("create-subscription"),
        {
            "plan": "pro-lifetime",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    subscription_obj = response.data["subscription"]
    assert subscription_obj["username"] == user.username
    assert subscription_obj["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(subscription_id=subscription_obj["id"])

    old_payment = payments.first()
    assert old_payment is not None
    old_subscription = Subscription.objects.get(pk=old_payment.subscription_id)

    response = authenticated_api_client.post(
        reverse("sync-subscription", kwargs={"pk": old_subscription.id}),
        format="json",
    )

    assert response.data["username"] == user.username
    assert response.data["status"] == SubscriptionStatus.ACTIVE

    payments = Payment.objects.filter(
        subscription_id=response.data["id"], status=PaymentStatus.SUCCEEDED
    )
    assert payments.count() == 1

    old_payment.refresh_from_db()
    old_subscription.refresh_from_db()

    assert old_payment.status == PaymentStatus.SUCCEEDED
    assert old_subscription.status == SubscriptionStatus.ACTIVE

    stripe_payment_intent_mock(id="test_intent_2")
    get_payment_intent_mock(
        id="test_intent_2", status=StripePaymentStatus.REQUIRES_PAYMENT
    )
    response = authenticated_api_client.post(
        reverse("create-subscription"),
        {
            "plan": "plus-lifetime",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    subscription_obj = response.data["subscription"]
    assert subscription_obj["username"] == user.username
    assert subscription_obj["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(subscription_id=subscription_obj["id"])
    assert payments.count() == 1

    payment = payments.first()
    assert payment is not None
    assert payment.status == PaymentStatus.PENDING

    subscription = Subscription.objects.get(pk=payment.subscription_id)
    assert subscription.status == SubscriptionStatus.PENDING

    stripe_webhook_event(
        event_type="payment_intent.succeeded",
        payment_intent_id=payment.stripe_payment_intent_id,
        payment_intent_status=PaymentStatus.SUCCEEDED,
    )

    response = authenticated_api_client.post(
        "/api/subscriptions/stripe/webhook/",
        data=b"{}",
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test-signature",
    )
    assert response.status_code == status.HTTP_200_OK

    payment.refresh_from_db()
    subscription.refresh_from_db()

    assert payment.status == PaymentStatus.SUCCEEDED
    assert subscription.status == SubscriptionStatus.ACTIVE

    old_subscription.refresh_from_db()
    assert old_subscription.status == SubscriptionStatus.CANCELED

    old_payment.refresh_from_db()
    assert old_payment.status == payment.status == PaymentStatus.SUCCEEDED


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_two_webhook_intents(
    authenticated_api_client: APIClient,
    user: User,
    stripe_webhook_event: Callable[..., stripe.Event],
    stripe_payment_intent_mock: Callable[..., stripe.Event],
    get_payment_intent_mock: Callable[..., stripe.Event],
    sync_subscription_status_mock: Callable[..., stripe.Event],
) -> None:
    stripe_payment_intent_mock()
    get_payment_intent_mock(status=StripePaymentStatus.SUCCEEDED)

    response = authenticated_api_client.post(
        reverse("create-subscription"),
        {
            "plan": "pro-lifetime",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    subscription_obj = response.data["subscription"]
    assert subscription_obj["username"] == user.username
    assert subscription_obj["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(subscription_id=subscription_obj["id"])

    payment = payments.first()
    assert payment is not None
    subscription = Subscription.objects.get(pk=payment.subscription_id)

    stripe_webhook_event(
        event_type="payment_intent.succeeded",
        payment_intent_id=payment.stripe_payment_intent_id,
        payment_intent_status=PaymentStatus.SUCCEEDED,
    )

    sync_subscription_status_mock(raise_error=True)
    response = authenticated_api_client.post(
        "/api/subscriptions/stripe/webhook/",
        data=b"{}",
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test-signature",
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    payment.refresh_from_db()
    subscription.refresh_from_db()

    assert payment.status == PaymentStatus.PENDING
    assert subscription.status == SubscriptionStatus.PENDING

    sync_subscription_status_mock(raise_error=False)
    response = authenticated_api_client.post(
        "/api/subscriptions/stripe/webhook/",
        data=b"{}",
        content_type="application/json",
        HTTP_STRIPE_SIGNATURE="test-signature",
    )
    assert response.status_code == status.HTTP_200_OK

    payment.refresh_from_db()
    subscription.refresh_from_db()

    assert payment.status == PaymentStatus.SUCCEEDED
    assert subscription.status == SubscriptionStatus.ACTIVE
