from django.urls import path

from app.agentia.views import AgentIaView, conversation

urlpatterns = [
    path("ai/agent/", AgentIaView.as_view(), name="ai-agent"),
    path(
        "conversations/",
        conversation.ConversationListView.as_view(),
        name="conversation-list",
    ),
    path(
        "conversations/<int:pk>/",
        conversation.ConversationDetailView.as_view(),
        name="conversation-detail",
    ),
    path(
        "conversation/messages/<int:pk>/",
        conversation.MessageDetailView.as_view(),
        name="message-detail",
    ),
    path(
        "conversation/messages/",
        conversation.MessageListView.as_view(),
        name="message-list",
    ),
]
