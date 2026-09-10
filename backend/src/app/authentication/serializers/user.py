from typing import Any

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer as BaseModelSerializer

from app.authentication.models import User
from app.subscription.models import StripeCustomer
from app.subscription.models.choices import SubscriptionStatus


class UserSerializer(BaseModelSerializer):
    """
    Serializer for the User model.
    """

    has_usable_password = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "pending_email",
            "subscription",
            "is_staff",
            "is_superuser",
            "has_usable_password",
            "avatar_url",
        )

    def get_has_usable_password(self, obj: User) -> bool:
        return obj.has_usable_password()

    def get_avatar_url(self, obj: User) -> str | None:
        if not obj.avatar:
            return None

        request = self.context.get("request")
        url = obj.avatar.url

        if request:
            return request.build_absolute_uri(url)
        return url

    def get_subscription(self, obj: User) -> dict[str, Any] | None:
        try:
            stripe_customer = obj.stripe_customer  # type: ignore
        except StripeCustomer.DoesNotExist:
            return None

        subscription = (
            stripe_customer.subscriptions.filter(
                status=SubscriptionStatus.ACTIVE,
            )
            .order_by("-created_at")
            .first()
        )
        if not subscription:
            return None

        from app.subscription.serializers.subscription import (
            MinimumSubscriptionSerializer,
        )

        return MinimumSubscriptionSerializer(subscription, context=self.context).data  # type: ignore
