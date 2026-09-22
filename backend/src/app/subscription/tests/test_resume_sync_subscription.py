from collections.abc import Callable

import pytest
import stripe
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from app.authentication.models import User
from app.subscription.models import (
    Payment,
    Subscription,
)
from app.subscription.models.choices import (
    PaymentStatus,
    StripePaymentStatus,
    SubscriptionStatus,
)


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_resume_subscription_success(
    authenticated_api_client: APIClient,
    user: User,
    stripe_payment_intent_mock: Callable[..., stripe.Event],
    get_payment_intent_mock: Callable[..., stripe.Event],
) -> None:
    stripe_payment_intent_mock()
    get_payment_intent_mock(status=StripePaymentStatus.REQUIRES_PAYMENT)

    response = authenticated_api_client.post(
        reverse("create-subscription"),
        {
            "plan": "plus-lifetime",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    subscription = response.data["subscription"]
    assert subscription["username"] == user.username
    assert subscription["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(subscription_id=subscription["id"])
    assert payments.count() == 1

    response = authenticated_api_client.post(
        reverse("resume-subscription", kwargs={"pk": subscription["id"]}),
        format="json",
    )

    subscription = response.data["subscription"]
    assert subscription["username"] == user.username
    assert subscription["status"] == SubscriptionStatus.PENDING

    assert response.data["client_secret"] == "test_intent_secret"


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_resume_active_subscription_fail(
    authenticated_api_client: APIClient,
    user: User,
    stripe_payment_intent_mock: Callable[..., stripe.Event],
    get_payment_intent_mock: Callable[..., stripe.Event],
) -> None:
    stripe_payment_intent_mock()
    get_payment_intent_mock(status=StripePaymentStatus.REQUIRES_PAYMENT)

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
    assert payments.count() == 1

    subscription = Subscription.objects.get(pk=subscription_obj["id"])

    subscription.status = SubscriptionStatus.ACTIVE
    subscription.current_period_start = timezone.now()
    subscription.save()

    assert subscription.is_lifetime

    response = authenticated_api_client.post(
        reverse("resume-subscription", kwargs={"pk": subscription.id}),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_resume_subscription_succeeded_payment_fail(
    authenticated_api_client: APIClient,
    user: User,
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

    subscription = response.data["subscription"]
    assert subscription["username"] == user.username
    assert subscription["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(subscription_id=subscription["id"])
    assert payments.count() == 1

    response = authenticated_api_client.post(
        reverse("resume-subscription", kwargs={"pk": subscription["id"]}),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_sync_subscription_succeeded_payment(
    authenticated_api_client: APIClient,
    user: User,
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

    payments = Payment.objects.filter(
        subscription_id=subscription_obj["id"], status=PaymentStatus.PENDING
    )
    assert payments.count() == 1

    subscription = Subscription.objects.get(pk=subscription_obj["id"])

    response = authenticated_api_client.post(
        reverse("sync-subscription", kwargs={"pk": subscription.id}),
        format="json",
    )

    assert response.data["username"] == user.username
    assert response.data["status"] == SubscriptionStatus.ACTIVE

    payments = Payment.objects.filter(
        subscription_id=response.data["id"], status=PaymentStatus.SUCCEEDED
    )
    assert payments.count() == 1


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_sync_subscription_pending_payment(
    authenticated_api_client: APIClient,
    user: User,
    stripe_payment_intent_mock: Callable[..., stripe.Event],
    get_payment_intent_mock: Callable[..., stripe.Event],
) -> None:
    stripe_payment_intent_mock()
    get_payment_intent_mock(status=StripePaymentStatus.REQUIRES_PAYMENT)

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

    payments = Payment.objects.filter(
        subscription_id=subscription_obj["id"], status=PaymentStatus.PENDING
    )
    assert payments.count() == 1

    subscription = Subscription.objects.get(pk=subscription_obj["id"])

    response = authenticated_api_client.post(
        reverse("sync-subscription", kwargs={"pk": subscription.id}),
        format="json",
    )

    assert response.data["username"] == user.username
    assert response.data["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(
        subscription_id=response.data["id"], status=PaymentStatus.PENDING
    )
    assert payments.count() == 1


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_sync_subscription_processing_payment(
    authenticated_api_client: APIClient,
    user: User,
    stripe_payment_intent_mock: Callable[..., stripe.Event],
    get_payment_intent_mock: Callable[..., stripe.Event],
) -> None:
    stripe_payment_intent_mock()
    get_payment_intent_mock(status=StripePaymentStatus.PROCESSING)

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

    payments = Payment.objects.filter(
        subscription_id=subscription_obj["id"], status=PaymentStatus.PENDING
    )
    assert payments.count() == 1

    subscription = Subscription.objects.get(pk=subscription_obj["id"])

    response = authenticated_api_client.post(
        reverse("sync-subscription", kwargs={"pk": subscription.id}),
        format="json",
    )

    assert response.data["username"] == user.username
    assert response.data["status"] == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(
        subscription_id=response.data["id"], status=PaymentStatus.PROCESSING
    )
    assert payments.count() == 1


@pytest.mark.django_db
@pytest.mark.usefixtures("get_stripe_customer_mock", "get_stripe_price_mock")
def test_sync_active_subscription_fail(
    authenticated_api_client: APIClient,
    user: User,
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
    assert payments.count() == 1

    subscription = Subscription.objects.get(pk=subscription_obj["id"])

    subscription.status = SubscriptionStatus.ACTIVE
    subscription.current_period_start = timezone.now()
    subscription.save()

    assert subscription.is_lifetime

    response = authenticated_api_client.post(
        reverse("sync-subscription", kwargs={"pk": subscription.id}),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data
