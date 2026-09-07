from typing import ClassVar

from django.conf import settings
from django.db import models

from app.core.models import BaseModel


class SubscriptionStatus(models.TextChoices):
    """Statuses defined for subscription model"""

    PENDING = "pending"
    ACTIVE = "active"
    CANCELED = "canceled"
    EXPIRED = "expired"


class StripeCustomer(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stripe_customer",
    )
    stripe_customer_id = models.CharField(max_length=255, unique=True)


class Subscription(BaseModel):
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.PENDING,
    )

    # Stripe
    stripe_customer = models.ForeignKey(
        StripeCustomer, on_delete=models.CASCADE, related_name="subscriptions"
    )
    stripe_subscription_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)

    # Period
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)

    @property
    def is_lifetime(self) -> bool:
        return (
            self.status == SubscriptionStatus.ACTIVE and self.current_period_end is None
        )

    class Meta:
        constraints: ClassVar = [
            models.CheckConstraint(
                condition=(
                    models.Q(current_period_end__isnull=True)
                    | models.Q(current_period_start__isnull=False)
                ),
                name="subscription_end_requires_start",
            ),
            models.CheckConstraint(
                condition=(
                    ~models.Q(status=SubscriptionStatus.ACTIVE)
                    | models.Q(current_period_start__isnull=False)
                ),
                name="active_subscription_requires_start",
            ),
            models.UniqueConstraint(
                fields=["stripe_customer", "stripe_price_id"],
                name="unique_subscription_per_customer_price",
            ),
        ]
