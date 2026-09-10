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
from app.subscription.models.choices import SubscriptionBilling
from app.subscription.serializers.subscription import (
    CancelSubscriptionSerializer,
    CreateSubscriptionSerializer,
    ResumeSubscriptionSerializer,
    SubscriptionPurchaseSerializer,
    SubscriptionSerializer,
    SyncSubscriptionSerializer,
)
from app.subscription.views.filters import SubscriptionFilter

logger = logging.getLogger(__name__)

# Products created in Stripe
STRIPE_PLANS = {
    "pro-lifetime": {
        "id": "pro-lifetime",
        "name": "Pro",
        "title": "Lifetime Pro Access",
        "amount": 29.99,
        "currency": "€",
        "billing": SubscriptionBilling.LIFE_TIME.label,
        "is_lifetime": True,
        "description": "Expanded capabilities and workspace features.",
        "stripe_price_id": settings.STRIPE_PRO_LIFETIME_PRICE_ID,
    },
    "plus-lifetime": {
        "id": "plus-lifetime",
        "name": "Plus",
        "title": "Lifetime Plus Access",
        "amount": 49.99,
        "currency": "€",
        "billing": SubscriptionBilling.LIFE_TIME.label,
        "is_lifetime": True,
        "description": "Highest performance tier with maximum speed and priority "
        "access.",
        "stripe_price_id": settings.STRIPE_PLUS_LIFETIME_PRICE_ID,
    },
}


@extend_schema(
    summary="List subscription plans",
    description="Return the available subscription plans.",
    tags=["Subscription"],
    responses={200: {"type": "list"}},
)
class SubscriptionPlansView(APIView):
    permission_classes = [AllowAny]  # noqa

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
        return Response(STRIPE_PLANS.values())


@extend_schema(
    summary="Retrieve subscription",
    description="Return one subscription belonging to the authenticated user.",
    tags=["Subscription"],
    responses={200: SubscriptionSerializer},
)
class SubscriptionDetailView(RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def get_queryset(self) -> QuerySet[Subscription]:  # pyright: ignore[reportIncompatibleMethodOverride]
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

    def get_queryset(self) -> QuerySet[Subscription]:  # pyright: ignore[reportIncompatibleMethodOverride]
        return Subscription.objects.filter(
            stripe_customer__user=self.request.user
        ).order_by("-created_at")


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

        logger.info(f"{user.username} started a purchase for the plan {plan}")
        return Response(
            SubscriptionPurchaseSerializer(data).data,
            status=201,
        )


@extend_schema(
    summary="Resume subscription",
    description="Resume the current pending subscription",
    request=ResumeSubscriptionSerializer,
    tags=["Subscription"],
    responses={200: SubscriptionPurchaseSerializer},
)
class ResumeSubscriptionView(APIView):
    serializer_class = ResumeSubscriptionSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user

        data = serializer.save(subscription_id=kwargs["pk"])

        logger.info(
            f"{user.username} resumed payment for the plan {data['subscription'].plan}"  # type: ignore
        )
        return Response(SubscriptionPurchaseSerializer(data).data, status=200)


@extend_schema(exclude=True)
class SyncSubscriptionView(APIView):
    serializer_class = SyncSubscriptionSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        subscription = serializer.save(subscription_id=kwargs["pk"])
        return Response(SubscriptionSerializer(subscription).data, status=200)


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

        logger.info(f"{user.username} canceled their plan {subscription.plan}")  # type: ignore
        return Response(SubscriptionSerializer(subscription).data, status=200)
