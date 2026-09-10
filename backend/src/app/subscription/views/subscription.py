import logging
from typing import Any

from django.conf import settings
from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.subscription.models import Subscription
from app.subscription.serializers.subscription import (
    CancelSubscriptionSerializer,
    CreateSubscriptionSerializer,
    SubscriptionPurchaseSerializer,
    SubscriptionSerializer,
)
from app.subscription.views.filters import SubscriptionFilter

logger = logging.getLogger(__name__)


@extend_schema(
    summary="List subscription plans",
    description="Return the available subscription plans.",
    tags=["Subscription"],
    responses={200: {"type": "dict"}},
)
class SubscriptionPlansView(APIView):
    permission_classes = [AllowAny]  # noqa

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
        return Response(settings.STRIPE_PLANS)


@extend_schema(
    summary="Retrieve subscription",
    description="Return one subscription belonging to the authenticated user.",
    tags=["Subscription"],
    responses={200: SubscriptionSerializer},
)
class SubscriptionDetailView(RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def get_queryset(self) -> QuerySet[Subscription]:
        return Subscription.objects.filter(stripe_customer__user=self.request.user)


@extend_schema(
    summary="List subscriptions",
    description="Return the subscriptions belonging to the authenticated user.",
    tags=["Subscription"],
    responses={200: SubscriptionSerializer(many=True)},
)
class SubscriptionListView(ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]  # noqa
    filterset_class = SubscriptionFilter

    def get_queryset(self) -> QuerySet[Subscription]:
        return Subscription.objects.filter(stripe_customer__user=self.request.user)


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
class CreateSubscriptionView(APIView):
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
    description="Cancel current subscription plan",
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
        return Response(SubscriptionSerializer(subscription).data, status=200)
