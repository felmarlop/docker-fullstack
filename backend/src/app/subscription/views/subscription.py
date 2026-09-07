import logging
from typing import Any

from django.conf import settings
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.subscription.serializers.subscription import (
    SubscriptionCreateSerializer,
    SubscriptionSerializer,
)
from app.subscription.stripe import api as stripe_api

logger = logging.getLogger(__name__)


@extend_schema(
    summary="Start subscription purchase",
    description="Start the purchase flow for a subscription plan.",
    request=SubscriptionCreateSerializer,
    tags=["Subscription"],
    responses={200: SubscriptionSerializer},
    examples=[
        OpenApiExample(
            "Subscription purchase request",
            value={
                "plan": "pro-lifetime",
            },
            request_only=True,
        ),
    ],
)
class SubscriptionView(APIView):
    serializer_class = SubscriptionCreateSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        plan = serializer.validated_data["plan"]  # type: ignore

        price_id = settings.STRIPE_PRICES[plan]
        price = stripe_api.get_price(price_id)

        logger.info(price)

        logger.info(f"{user.username} started a purchase for the subscription {plan}")
        return Response({})  # type: ignore
