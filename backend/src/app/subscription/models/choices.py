from django.db import models


class SubscriptionStatus(models.TextChoices):
    """Statuses defined for subscription model"""

    PENDING = "pending"
    ACTIVE = "active"
    CANCELED = "canceled"
    EXPIRED = "expired"


class SubscriptionBilling(models.TextChoices):
    """Billing defined for a plan"""

    LIFE_TIME = "one-time", "One-time"
    MONTHLY = "monthly", "Monthly"
    YEARLY = "yearly", "Yearly"


class PaymentStatus(models.TextChoices):
    """Statuses defined for subscription model"""

    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"


class StripePaymentStatus(models.TextChoices):
    REQUIRES_PAYMENT = "requires_payment_method"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    REQUIRES_ACTION = "requires_action"
    REQUIRES_CAPTURE = "requires_capture"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    CANCELED = "canceled"


STRIPE_PAYMENT_STATUS_MAP = {
    StripePaymentStatus.REQUIRES_PAYMENT: PaymentStatus.PENDING,
    StripePaymentStatus.REQUIRES_CONFIRMATION: PaymentStatus.PENDING,
    StripePaymentStatus.REQUIRES_ACTION: PaymentStatus.PENDING,
    StripePaymentStatus.PROCESSING: PaymentStatus.PROCESSING,
    StripePaymentStatus.SUCCEEDED: PaymentStatus.SUCCEEDED,
    StripePaymentStatus.CANCELED: PaymentStatus.CANCELED,
}

PAYMENT_TO_SUBSCRIPTION_STATUS = {
    PaymentStatus.PENDING: SubscriptionStatus.PENDING,
    PaymentStatus.PROCESSING: SubscriptionStatus.PENDING,
    PaymentStatus.SUCCEEDED: SubscriptionStatus.ACTIVE,
    PaymentStatus.FAILED: SubscriptionStatus.PENDING,
    PaymentStatus.CANCELED: SubscriptionStatus.CANCELED,
}
