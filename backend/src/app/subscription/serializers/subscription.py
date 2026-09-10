from typing import Any

import stripe
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from app.authentication.models import User
from app.subscription.models import (
    Payment,
    PaymentStatus,
    StripeCustomer,
    Subscription,
    SubscriptionStatus,
)
from app.subscription.stripe import api as stripe_api


class CreateSubscriptionSerializer(serializers.Serializer):
    plan = serializers.CharField()

    def _get_or_create_customer(self, user: User) -> StripeCustomer:
        try:
            customer = user.stripe_customer  # type: ignore
            stripe_customer = stripe_api.get_customer(customer.stripe_customer_id)
        except StripeCustomer.DoesNotExist:
            stripe_customer = stripe_api.create_customer(user)
            customer = StripeCustomer.objects.create(
                user=user,
                stripe_customer_id=stripe_customer.id,
            )

        if getattr(stripe_customer, "deleted", False):
            stripe_customer = stripe_api.create_customer(user)
            customer.stripe_customer_id = stripe_customer.id
            customer.save(update_fields=["stripe_customer_id"])

        return customer

    def validate_plan(self, value: str) -> str:
        if value not in settings.STRIPE_PLANS:
            raise serializers.ValidationError("Invalid subscription plan.")
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        user = self.context["request"].user

        if Subscription.objects.filter(
            stripe_customer__user=user,
            plan=attrs["plan"],
            status__in=[
                SubscriptionStatus.PENDING,
                SubscriptionStatus.ACTIVE,
            ],
        ).exists():
            raise serializers.ValidationError(
                {"detail": ["User already has this subscription."]}
            )

        return attrs

    def create(self, validated_data: dict[str, Any]) -> dict[str, Any]:
        plan = validated_data.pop("plan")
        user = self.context["request"].user

        price_id = settings.STRIPE_PLANS[plan]["stripe_price_id"]
        price = stripe_api.get_price(price_id)

        customer = self._get_or_create_customer(user)

        product_name = "Product"
        if isinstance(price.product, stripe.Product):
            product_name = price.product.name

        with transaction.atomic():
            subscription = Subscription.objects.create(
                name=f"{product_name} - {price.id}",
                plan=plan,
                stripe_customer=customer,
                stripe_price_id=price.id,
            )

            payment_intent = stripe_api.create_payment_intent(price, subscription)  # type: ignore
            Payment.objects.create(
                subscription=subscription,
                stripe_payment_intent_id=payment_intent.id,
                amount=payment_intent.amount,
                currency=payment_intent.currency,
            )

        return {
            "subscription": subscription,
            "client_secret": payment_intent.client_secret,
        }


class CancelSubscriptionSerializer(serializers.Serializer):
    confirmation = serializers.CharField()

    def validate_confirmation(self, value: str) -> str:
        if value != "CANCEL":
            raise serializers.ValidationError('Please type "CANCEL" to confirm.')
        return value

    def save(self, subscription_id: int, **kwargs: Any) -> Subscription:  # noqa: ARG002
        user = self.context["request"].user
        subscription_to_cancel = get_object_or_404(
            Subscription, id=subscription_id, stripe_customer__user=user
        )

        if subscription_to_cancel.status in [
            SubscriptionStatus.CANCELED,
            SubscriptionStatus.EXPIRED,
        ]:
            raise serializers.ValidationError(
                {
                    "detail": [
                        "Canceled or expired subscriptions cannot be canceled again."
                    ]
                }
            )

        if subscription_to_cancel.is_lifetime:
            raise serializers.ValidationError(
                {"detail": ["Active lifetime subscriptions cannot be canceled."]}
            )

        with transaction.atomic():
            pending_payments = subscription_to_cancel.payments.filter(  # type: ignore
                status=PaymentStatus.PENDING
            )
            for p in pending_payments:
                stripe_api.cancel_payment_intent(p.stripe_payment_intent_id)

                p.status = PaymentStatus.CANCELED
                p.save(update_fields=["status", "updated_at"])

            subscription_to_cancel.status = SubscriptionStatus.CANCELED

            if subscription_to_cancel.current_period_start:
                subscription_to_cancel.current_period_end = timezone.now()

            subscription_to_cancel.save(
                update_fields=["status", "current_period_end", "updated_at"]
            )

        return subscription_to_cancel


class SubscriptionSerializer(serializers.ModelSerializer):
    is_lifetime = serializers.BooleanField(read_only=True)
    username = serializers.CharField(
        source="stripe_customer.user.username",
        read_only=True,
    )

    class Meta:
        model = Subscription
        fields = (
            "id",
            "name",
            "plan",
            "status",
            "username",
            "current_period_start",
            "current_period_end",
            "is_lifetime",
            "created_at",
            "updated_at",
        )


class SubscriptionPurchaseSerializer(serializers.Serializer):
    subscription = SubscriptionSerializer()
    client_secret = serializers.CharField()
