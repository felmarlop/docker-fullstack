from typing import ClassVar

from django.db import models

from app.core.models import BaseModel
from app.subscription.models import subscription
from app.subscription.models.choices import PaymentStatus


class Payment(BaseModel):
    subscription = models.ForeignKey(
        subscription.Subscription,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    # Stripe
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        unique=True,
    )

    # Payment
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=3)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:  # type: ignore
        constraints: ClassVar = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="payment_amount_gt_0",
            ),
        ]
