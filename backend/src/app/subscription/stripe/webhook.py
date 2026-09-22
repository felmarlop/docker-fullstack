import logging
from typing import Any

import stripe
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.subscription import services
from app.subscription.models import Payment

logger = logging.getLogger(__name__)


@extend_schema(exclude=True)
class StripWebhookView(APIView):
    authentication_classes = []  # noqa
    permission_classes = [AllowAny]  # noqa

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
        event = None
        payment_intent = None
        try:
            event = stripe.Webhook.construct_event(
                payload=request.body,
                sig_header=request.headers.get("Stripe-Signature"),
                secret=settings.STRIPE_WEBHOOK_SECRET,
            )

            payment_intent = event.data.object
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent.id)

            services.sync_subscription_status(
                payment.subscription_id,  # type: ignore
                payment_intent.status,
            )
        except (ValueError, stripe.SignatureVerificationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            if payment_intent:
                logger.exception(
                    "Payment not found for Stripe PaymentIntent %s.",
                    payment_intent.id,
                )
            else:
                logger.exception("Payment not found")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            logger.exception("Failed to process Stripe webhook.")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)
