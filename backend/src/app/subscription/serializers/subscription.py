from typing import Any

import stripe
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from app.authentication.models import User
from app.subscription import services
from app.subscription.models import (
    Payment,
    StripeCustomer,
    Subscription,
)
from app.subscription.models.choices import (
    PaymentStatus,
    SubscriptionStatus,
)
from app.subscription.stripe import api as stripe_api
from app.subscription.views import subscription as s_views


class MinimumSubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            "plan",
            "plan_name",
            "status",
        )

    def get_plan_name(self, obj: Subscription) -> str:
        return s_views.STRIPE_PLANS[obj.plan]["name"]


class SubscriptionSerializer(MinimumSubscriptionSerializer):
    is_lifetime = serializers.BooleanField(read_only=True)
    payment_status = serializers.SerializerMethodField()
    username = serializers.CharField(
        source="stripe_customer.user.username",
        read_only=True,
    )

    class Meta(MinimumSubscriptionSerializer.Meta):
        fields = (
            *MinimumSubscriptionSerializer.Meta.fields,
            "id",
            "name",
            "username",
            "is_lifetime",
            "payment_status",
            "current_period_start",
            "current_period_end",
            "created_at",
            "updated_at",
        )

    def get_payment_status(self, obj: Subscription) -> str | None:
        payment = obj.payments.order_by("-created_at").first()  # type: ignore
        return payment.status if payment else None


class SubscriptionPurchaseSerializer(serializers.Serializer):
    subscription = SubscriptionSerializer()
    client_secret = serializers.CharField()


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

    def _cancel_pending_subscriptions(self) -> None:
        user = self.context["request"].user
        pending_subscriptions = Subscription.objects.filter(
            stripe_customer__user=user,
            status=SubscriptionStatus.PENDING,
        )

        for pending_subscription in pending_subscriptions:
            services.cancel_subscription(pending_subscription)

    def validate_plan(self, value: str) -> str:
        if value not in s_views.STRIPE_PLANS:
            raise serializers.ValidationError("Invalid subscription plan.")
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        user = self.context["request"].user

        if Subscription.objects.filter(
            stripe_customer__user=user,
            plan=attrs["plan"],
            status=SubscriptionStatus.ACTIVE,
        ).exists():
            raise serializers.ValidationError(
                {"detail": ["User already has this subscription."]}
            )

        return attrs

    def create(self, validated_data: dict[str, Any]) -> dict[str, Any]:
        plan = validated_data.pop("plan")
        user = self.context["request"].user

        price_id = s_views.STRIPE_PLANS[plan]["stripe_price_id"]
        price = stripe_api.get_price(price_id)

        customer = self._get_or_create_customer(user)

        self._cancel_pending_subscriptions()

        product_name = "Product"
        if isinstance(price.product, stripe.Product):
            product_name = price.product.name

        with transaction.atomic():
            subscription = Subscription.objects.create(
                name=f"{product_name}",
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


class ResumeSubscriptionSerializer(serializers.Serializer):
    def save(self, subscription_id: int, **kwargs: Any) -> dict[str, Any]:  # noqa: ARG002 # pyright: ignore[reportIncompatibleMethodOverride]
        user = self.context["request"].user
        subscription_to_resume = get_object_or_404(
            Subscription, id=subscription_id, stripe_customer__user=user
        )

        if subscription_to_resume.status != SubscriptionStatus.PENDING:
            raise serializers.ValidationError(
                {"detail": ["Only pending subscriptions can be resumed."]}
            )

        payment_to_resume = Payment.objects.filter(
            subscription=subscription_to_resume, status=PaymentStatus.PENDING
        ).first()

        if not payment_to_resume:
            raise serializers.ValidationError({"detail": ["No pending payment found."]})

        payment_intent = stripe_api.get_resumable_payment_intent(
            payment_to_resume.stripe_payment_intent_id
        )
        return {
            "subscription": subscription_to_resume,
            "client_secret": payment_intent.client_secret,
        }


class SyncSubscriptionSerializer(serializers.Serializer):
    def save(self, subscription_id: int, **kwargs: Any) -> Subscription:  # noqa: ARG002 # pyright: ignore[reportIncompatibleMethodOverride]
        user = self.context["request"].user
        subscription_to_sync = get_object_or_404(
            Subscription, id=subscription_id, stripe_customer__user=user
        )

        if subscription_to_sync.status != SubscriptionStatus.PENDING:
            raise serializers.ValidationError(
                {"detail": ["Only pending subscriptions can be synchronized."]}
            )

        return services.sync_subscription_status(subscription_to_sync.pk)


class CancelSubscriptionSerializer(serializers.Serializer):
    confirmation = serializers.CharField()

    def validate_confirmation(self, value: str) -> str:
        if value != "CANCEL":
            raise serializers.ValidationError('Please type "CANCEL" to confirm.')
        return value

    def save(self, subscription_id: int, **kwargs: Any) -> Subscription:  # noqa: ARG002 # pyright: ignore[reportIncompatibleMethodOverride]
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

        return services.cancel_subscription(subscription_to_cancel)
