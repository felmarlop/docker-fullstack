from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from app.agentia.models import Conversation, Message
from app.agentia.serializers.conversation import (
    ConversationSerializer,
    MessageSerializer,
    MinimumConversationSerializer,
    MinimumMessageSerializer,
)
from app.agentia.views.filters import MessageFilter
from app.core.pagination import DefaultPagination


@extend_schema(
    summary="Retrieve conversation",
    description="Return one conversation belonging to the authenticated user.",
    tags=["AgentIA"],
    responses={200: ConversationSerializer},
)
class ConversationDetailView(RetrieveAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def get_queryset(self) -> QuerySet[Conversation]:  # pyright: ignore[reportIncompatibleMethodOverride]
        return Conversation.objects.filter(user=self.request.user)


@extend_schema(
    summary="List conversations",
    description="Return the conversations belonging to the authenticated user.",
    tags=["AgentIA"],
    responses={200: MinimumConversationSerializer(many=True)},
)
class ConversationListView(ListAPIView):
    serializer_class = MinimumConversationSerializer
    permission_classes = [IsAuthenticated]  # noqa
    filter_backends = [DjangoFilterBackend]  # noqa
    pagination_class = DefaultPagination

    def get_queryset(self) -> QuerySet[Conversation]:  # pyright: ignore[reportIncompatibleMethodOverride]
        return Conversation.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


@extend_schema(
    summary="Retrieve message",
    description="Return one message belonging to the authenticated user.",
    tags=["AgentIA"],
    responses={200: MessageSerializer},
)
class MessageDetailView(RetrieveAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def get_queryset(self) -> QuerySet[Message]:  # pyright: ignore[reportIncompatibleMethodOverride]
        return Message.objects.filter(conversation__user=self.request.user)


@extend_schema(
    summary="List messages",
    description="Return the messages belonging to the user's conversations.",
    tags=["AgentIA"],
    responses={200: MinimumMessageSerializer(many=True)},
)
class MessageListView(ListAPIView):
    serializer_class = MinimumMessageSerializer
    permission_classes = [IsAuthenticated]  # noqa
    filterset_class = MessageFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # noqa
    ordering_fields = ["created_at"]  # noqa
    ordering = ["-created_at"]  # noqa
    pagination_class = DefaultPagination

    def get_queryset(self) -> QuerySet[Message]:  # pyright: ignore[reportIncompatibleMethodOverride]
        return Message.objects.filter(conversation__user=self.request.user).order_by(
            "-created_at"
        )
