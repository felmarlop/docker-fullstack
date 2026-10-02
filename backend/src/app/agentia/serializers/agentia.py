import logging

from rest_framework import serializers

from app.agentia.api import api as AgentApi
from app.agentia.models import Conversation, Message
from app.agentia.models.choices import MessageRole
from app.agentia.serializers import conversation
from app.authentication.models import User

logger = logging.getLogger(__name__)

PROMPT_SPLITS = 20


class AgentIaRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField()

    def _create_message(self, user: User, content: str, role: MessageRole) -> Message:

        conversation, _ = Conversation.objects.get_or_create(user=user)
        if not conversation.name:
            conversation.name = " ".join(content.split()[:5])
            conversation.save(update_fields=["name"])

        return Message.objects.create(
            content=content, conversation=conversation, role=role
        )

    def send_message(self) -> tuple[Message, Message]:
        user = self.context["request"].user

        prompt = str(self.validated_data["prompt"])  # type: ignore
        prompt_msg = self._create_message(user, prompt, MessageRole.USER)

        logger.info(
            f"{user.username} sent a prompt to AgentIA: {prompt[:PROMPT_SPLITS]} ...",
        )

        answer = AgentApi.send_message(prompt)
        answer_msg = self._create_message(user, answer, MessageRole.ASSISTANT)

        return answer_msg, prompt_msg


class AgentIaAnswerSerializer(serializers.Serializer):
    prompt = conversation.MessageSerializer()
    answer = conversation.MessageSerializer()
