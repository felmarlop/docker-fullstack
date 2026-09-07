import stripe
from django.conf import settings

from app.subscription.stripe.exceptions import StripePriceNotActive, StripePriceNotFound


class StripeAPI:
    def __init__(self) -> None:
        self.client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)

    def get_price(self, price_id: str) -> stripe.Price:
        try:
            price = self.client.v1.prices.retrieve(
                price_id,
                params={"expand": ["product"]},
            )
        except stripe.InvalidRequestError as exc:
            raise StripePriceNotFound from exc

        if not price.active:
            raise StripePriceNotActive

        return price
