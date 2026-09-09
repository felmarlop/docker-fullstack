import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from app.authentication.models import User
from app.subscription.models import (
    Payment,
    PaymentStatus,
    Subscription,
    SubscriptionStatus,
)


@pytest.mark.django_db
@pytest.mark.usefixtures("stripe_payment_intent_mock")
def test_create_subscription_success(
    authenticated_api_client: APIClient,
    user: User,
) -> None:
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

    assert response.data["client_secret"] == "test_intent_secret"

    payments = Payment.objects.filter(subscription_id=subscription["id"])
    assert payments.count() == 1

    payment = payments.first()
    assert payment.status == PaymentStatus.PENDING
    assert payment.stripe_payment_intent_id == "test_intent"


@pytest.mark.django_db
def test_create_subscription_invalid_plan(authenticated_api_client: APIClient) -> None:
    response = authenticated_api_client.post(
        reverse("create-subscription"),
        {
            "plan": "pro-lifetime-wrong",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "plan" in response.data

    assert Payment.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.usefixtures(
    "stripe_payment_intent_mock", "stripe_cancel_payment_intent_mock"
)
def test_cancel_subscription_success(
    authenticated_api_client: APIClient, user: User
) -> None:
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

    payment = payments.first()
    assert payment.status == PaymentStatus.PENDING
    assert payment.stripe_payment_intent_id == "test_intent"

    response = authenticated_api_client.post(
        reverse("cancel-subscription", kwargs={"pk": subscription["id"]}),
        {
            "confirmation": "CANCEL",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username
    assert response.data["status"] == SubscriptionStatus.CANCELED

    payments = Payment.objects.filter(subscription_id=response.data["id"])
    assert payments.count() == 1

    payment = payments.first()
    assert payment.status == PaymentStatus.CANCELED


@pytest.mark.django_db
@pytest.mark.usefixtures("stripe_payment_intent_mock")
def test_cancel_subscription_invalid_pk(
    authenticated_api_client: APIClient, user: User
) -> None:
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

    payment = payments.first()
    assert payment.status == PaymentStatus.PENDING
    assert payment.stripe_payment_intent_id == "test_intent"

    response = authenticated_api_client.post(
        reverse("cancel-subscription", kwargs={"pk": 0}),
        {
            "confirmation": "CANCEL",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.data


@pytest.mark.django_db
@pytest.mark.usefixtures("stripe_payment_intent_mock")
def test_cancel_subscription_invalid_confirmation(
    authenticated_api_client: APIClient, user: User
) -> None:
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

    payment = payments.first()
    assert payment.status == PaymentStatus.PENDING
    assert payment.stripe_payment_intent_id == "test_intent"

    response = authenticated_api_client.post(
        reverse("cancel-subscription", kwargs={"pk": subscription["id"]}),
        {
            "confirmation": "DELETE",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "confirmation" in response.data


@pytest.mark.django_db
@pytest.mark.usefixtures(
    "stripe_payment_intent_mock", "stripe_cancel_payment_intent_mock"
)
def test_cancel_subscription_twice(
    authenticated_api_client: APIClient, user: User
) -> None:
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

    payment = payments.first()
    assert payment.status == PaymentStatus.PENDING
    assert payment.stripe_payment_intent_id == "test_intent"

    response = authenticated_api_client.post(
        reverse("cancel-subscription", kwargs={"pk": subscription["id"]}),
        {
            "confirmation": "CANCEL",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username
    assert response.data["status"] == SubscriptionStatus.CANCELED

    payments = Payment.objects.filter(subscription_id=response.data["id"])
    assert payments.count() == 1

    payment = payments.first()
    assert payment.status == PaymentStatus.CANCELED

    response = authenticated_api_client.post(
        reverse("cancel-subscription", kwargs={"pk": response.data["id"]}),
        {
            "confirmation": "CANCEL",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data


@pytest.mark.django_db
@pytest.mark.usefixtures(
    "stripe_payment_intent_mock", "stripe_cancel_payment_intent_mock"
)
def test_cancel_lifetime_subscription_fail(
    authenticated_api_client: APIClient, user: User
) -> None:
    response = authenticated_api_client.post(
        reverse("create-subscription"),
        {
            "plan": "pro-lifetime",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    subscription_obj = response.data["subscription"]
    subscription = Subscription.objects.get(pk=subscription_obj["id"])

    assert subscription.stripe_customer.user.username == user.username
    assert subscription.status == SubscriptionStatus.PENDING

    payments = Payment.objects.filter(subscription_id=subscription.id)
    assert payments.count() == 1

    payment = payments.first()
    assert payment.status == PaymentStatus.PENDING
    assert payment.stripe_payment_intent_id == "test_intent"

    subscription.status = SubscriptionStatus.ACTIVE
    subscription.current_period_start = timezone.now()
    subscription.save()

    assert subscription.is_lifetime

    response = authenticated_api_client.post(
        reverse("cancel-subscription", kwargs={"pk": subscription.id}),
        {
            "confirmation": "CANCEL",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.data
