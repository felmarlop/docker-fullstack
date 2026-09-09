import logging
from typing import Any

from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.subscription.serializers.subscription import (
    CancelSubscriptionSerializer,
    CreateSubscriptionSerializer,
    SubscriptionPurchaseSerializer,
    SubscriptionSerializer,
)

logger = logging.getLogger(__name__)


@extend_schema(
    summary="Start subscription purchase",
    description="Start the purchase flow for a subscription plan.",
    request=CreateSubscriptionSerializer,
    tags=["Subscription"],
    responses={201: SubscriptionPurchaseSerializer},
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
    serializer_class = CreateSubscriptionSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        plan = serializer.validated_data["plan"]  # type: ignore

        data = serializer.save()

        logger.info(f"{user.username} started a purchase for the subscription {plan}")
        return Response(
            SubscriptionPurchaseSerializer(data).data,
            status=201,
        )


@extend_schema(
    summary="Cancel subscription",
    description="Cancel subscription",
    request=CancelSubscriptionSerializer,
    tags=["Subscription"],
    responses={200: SubscriptionSerializer},
    examples=[
        OpenApiExample(
            "Cancel subscription request",
            value={
                "confirmation": "CANCEL",
            },
            request_only=True,
        ),
    ],
)
class CancelSubscriptionView(APIView):
    serializer_class = CancelSubscriptionSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user

        subscription = serializer.save(subscription_id=kwargs["pk"])

        logger.info(f"{user.username} cancel their subscription {subscription.id}")  # type: ignore
        return Response(
            SubscriptionSerializer(subscription).data,
            status=200,
        )
