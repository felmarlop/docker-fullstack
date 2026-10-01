import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.agentia.models import Conversation, Message
from app.agentia.models.choices import MessageRole
from app.authentication.models import User


@pytest.mark.django_db
def test_conversation_and_messages(
    authenticated_api_client: APIClient, user: User
) -> None:
    prompt_1 = "hello!"
    prompt_2 = "reply only with `Great job!`"
    response = authenticated_api_client.post(
        reverse("ai-agent"),
        {
            "prompt": prompt_1,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "prompt" in response.data
    assert "answer" in response.data

    response = authenticated_api_client.post(
        reverse("ai-agent"),
        {
            "prompt": prompt_2,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["answer"]["content"] == "Great job!"

    conversations = Conversation.objects.filter(user=user)
    assert conversations.exists()
    assert conversations.count() == 1

    conversation = conversations.first()
    assert conversation is not None

    message_qs = Message.objects.filter(conversation=conversation)
    assert message_qs.count() == 4

    user_message_qs = message_qs.filter(role=MessageRole.USER)
    ai_message_qs = message_qs.filter(role=MessageRole.ASSISTANT)
    assert user_message_qs.count() == 2
    assert ai_message_qs.count() == 2

    assert user_message_qs.first().content == prompt_1
    assert ai_message_qs.last().content == "Great job!"
