import logging

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from app.subscription import tasks
from app.subscription.models import Payment, Subscription
from app.subscription.models.choices import (
    PAYMENT_TO_SUBSCRIPTION_STATUS,
    STRIPE_PAYMENT_STATUS_MAP,
    PaymentStatus,
    StripePaymentStatus,
    SubscriptionStatus,
)
from app.subscription.stripe import api as stripe_api
from app.subscription.stripe.exceptions import StripeGeneralError

logger = logging.getLogger(__name__)


def send_subscription_activation(subscription_id: int) -> None:
    tasks.send_active_subscription_email.delay(subscription_id)  # pyright: ignore[reportFunctionMemberAccess]


def sync_subscription_status(
    subscription_id: int, payment_intent_status: str | None = None
) -> Subscription:
    """
    Synchronize a subscription and its latest payment with Stripe.

    Retrieve the latest PaymentIntent and update the local payment status.
    If a pending subscription becomes active, cancel the user's previous
    active subscriptions, and send an email after the database transaction commits.
    """

    def _get_payment(subscription_id: int) -> Payment:
        payment = (
            Payment.objects.filter(subscription_id=subscription_id)
            .order_by("-created_at")
            .first()
        )
        if payment is None:
            raise ValidationError(
                {"detail": ["No payment found associated to the subscription."]}
            )
        return payment

    def _cancel_active_subscriptions(current_subscription: Subscription) -> None:
        user = current_subscription.stripe_customer.user
        old_subscriptions = Subscription.objects.filter(
            stripe_customer__user=user,
            status=SubscriptionStatus.ACTIVE,
        ).exclude(pk=current_subscription.pk)

        for old_subscription in old_subscriptions:
            cancel_subscription(old_subscription)

    payment = _get_payment(subscription_id)
    if payment and not payment_intent_status:
        payment_intent = stripe_api.get_payment_intent(payment.stripe_payment_intent_id)
        payment_intent_status = payment_intent.status

    with transaction.atomic():
        # block instances before updating them
        subscription = Subscription.objects.select_for_update().get(pk=subscription_id)
        payment = Payment.objects.select_for_update().get(
            pk=payment.pk, subscription_id=subscription_id
        )

        was_pending = subscription.status == SubscriptionStatus.PENDING
        was_succeeded = payment.status == PaymentStatus.SUCCEEDED

        if not was_succeeded:
            payment.status = STRIPE_PAYMENT_STATUS_MAP.get(
                payment_intent_status,  # type: ignore
                PaymentStatus.PROCESSING,
            )
            if payment.status == PaymentStatus.SUCCEEDED and payment.paid_at is None:
                payment.paid_at = timezone.now()
            payment.save(update_fields=["status", "paid_at", "updated_at"])

        if was_pending:
            subscription.status = PAYMENT_TO_SUBSCRIPTION_STATUS.get(
                payment.status, SubscriptionStatus.PENDING
            )

            if is_active := subscription.status == SubscriptionStatus.ACTIVE:
                _cancel_active_subscriptions(subscription)
                if subscription.current_period_start is None:
                    subscription.current_period_start = timezone.now()

                transaction.on_commit(
                    lambda: send_subscription_activation(subscription.pk)
                )

            subscription.save(
                update_fields=["status", "current_period_start", "updated_at"]
            )

            if is_active:
                user = subscription.stripe_customer.user
                logger.info(f"Plan {subscription.plan} activated for {user.username}")

    return subscription


def cancel_subscription(subscription: Subscription) -> Subscription:
    """
    Cancel a subscription and reconcile its pending payments with Stripe.

    Attempt to cancel pending PaymentIntents and update their local statuses
    according to Stripe's response. Log individual payment cancellation
    failures without preventing the subscription from being canceled.
    """

    def _cancel_pending_payments(current_subscription: Subscription) -> None:
        pending_payments = current_subscription.payments.filter(  # type: ignore
            status=PaymentStatus.PENDING
        )
        for p in pending_payments:
            try:
                intent = stripe_api.cancel_payment_intent(p.stripe_payment_intent_id)
            except StripeGeneralError:
                logger.exception(
                    "Failed to cancel payment %s in Stripe.",
                    p.pk,
                )
                continue

            if intent.status == StripePaymentStatus.SUCCEEDED:
                p.status = PaymentStatus.SUCCEEDED
                if p.paid_at is None:
                    p.paid_at = timezone.now()
            elif intent.status == StripePaymentStatus.CANCELED:
                p.status = PaymentStatus.CANCELED
            else:
                logger.warning(
                    "Could not cancel payment %s in Stripe (status=%s).",
                    p.pk,
                    intent.status,
                )
                continue

            p.save(update_fields=["status", "paid_at", "updated_at"])

    with transaction.atomic():
        _cancel_pending_payments(subscription)
        if subscription.status not in [
            SubscriptionStatus.CANCELED,
            SubscriptionStatus.EXPIRED,
        ]:
            subscription.status = SubscriptionStatus.CANCELED

            if subscription.current_period_start:
                subscription.current_period_end = timezone.now()

            subscription.save(
                update_fields=["status", "current_period_end", "updated_at"]
            )
    return subscription
