import stripe
from django.conf import settings

from app.authentication.models import User
from app.subscription.models import Subscription
from app.subscription.models.choices import StripePaymentStatus
from app.subscription.stripe.exceptions import (
    StripeGeneralError,
    StripePaymentCannotBeResumed,
    StripePaymentNotFound,
    StripePriceNoAmount,
    StripePriceNotActive,
    StripePriceNotFound,
)


class StripeAPI:
    def __init__(self) -> None:
        self.client = stripe.StripeClient(settings.STRIPE_SECRET_KEY).v1

    def get_price(self, price_id: str) -> stripe.Price:
        if not price_id:
            raise StripePriceNotFound

        try:
            price = self.client.prices.retrieve(
                price_id,
                params={"expand": ["product"]},
            )
        except stripe.InvalidRequestError as exc:
            raise StripePriceNotFound from exc

        if not price.active:
            raise StripePriceNotActive

        return price

    def create_customer(self, user: User) -> stripe.Customer:
        try:
            return self.client.customers.create(
                params={
                    "email": user.email,
                    "name": user.username,
                    "metadata": {"user_id": str(user.pk)},
                }
            )
        except stripe.StripeError as exc:
            raise StripeGeneralError from exc

    def get_customer(self, customer_id: str) -> stripe.Customer:
        try:
            return self.client.customers.retrieve(customer_id)
        except stripe.StripeError as exc:
            raise StripeGeneralError from exc

    def create_payment_intent(
        self, price: stripe.Price, subscription: Subscription
    ) -> stripe.PaymentIntent:
        if price.unit_amount is None:
            raise StripePriceNoAmount

        try:
            return self.client.payment_intents.create(
                params={
                    "amount": price.unit_amount,
                    "currency": price.currency,
                    "customer": subscription.stripe_customer.stripe_customer_id,
                    "payment_method_types": ["card"],
                }
            )
        except stripe.StripeError as exc:
            raise StripeGeneralError from exc

    def get_payment_intent(self, payment_intent_id: str) -> stripe.PaymentIntent:
        try:
            return self.client.payment_intents.retrieve(payment_intent_id)
        except stripe.InvalidRequestError as exc:
            raise StripePaymentNotFound from exc

    def get_resumable_payment_intent(
        self, payment_intent_id: str
    ) -> stripe.PaymentIntent:
        payment_intent = self.get_payment_intent(payment_intent_id)
        if payment_intent.status not in [
            StripePaymentStatus.REQUIRES_PAYMENT,
            StripePaymentStatus.REQUIRES_CONFIRMATION,
        ]:
            raise StripePaymentCannotBeResumed
        return payment_intent

    def cancel_payment_intent(self, payment_intent_id: str) -> stripe.PaymentIntent:
        try:
            intent = self.get_payment_intent(payment_intent_id)
            if intent.status in [
                StripePaymentStatus.SUCCEEDED,
                StripePaymentStatus.CANCELED,
            ]:
                return intent

            return self.client.payment_intents.cancel(
                payment_intent_id,
                params={
                    "cancellation_reason": "requested_by_customer",
                },
            )
        except stripe.StripeError as exc:
            raise StripeGeneralError from exc
