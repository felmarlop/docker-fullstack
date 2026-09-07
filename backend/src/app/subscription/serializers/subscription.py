from typing import Any

from django.conf import settings
from rest_framework import serializers

from app.subscription.models import subscription


class SubscriptionCreateSerializer(serializers.Serializer):
    plan = serializers.CharField()

    def validate_plan(self, value: str) -> str:
        if value not in settings.STRIPE_PRICES:
            raise serializers.ValidationError("Invalid subscription plan.")
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        user = self.context["request"].user
        price_id = settings.STRIPE_PRICES[attrs["plan"]]

        if subscription.Subscription.objects.filter(
            stripe_customer__user=user,
            stripe_price_id=price_id,
        ).exists():
            raise serializers.ValidationError("User already has this subscription.")

        return attrs


class SubscriptionSerializer(serializers.ModelSerializer):
    is_lifetime = serializers.BooleanField(read_only=True)
    username = serializers.CharField(
        source="stripe_customer.user.username",
        read_only=True,
    )

    class Meta:
        model = subscription.Subscription
        fields = (
            "id",
            "name",
            "status",
            "username",
            "stripe_price_id",
            "current_period_start",
            "current_period_end",
            "is_lifetime",
            "created_at",
            "updated_at",
        )
