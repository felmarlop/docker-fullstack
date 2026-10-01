import logging

from rest_framework import serializers

from app.agentia.api import api as GeminiApi
from app.agentia.models import Conversation, Message
from app.agentia.models.choices import MessageRole
from app.agentia.serializers import conversation

logger = logging.getLogger(__name__)

PROMPT_SPLITS = 20


class AgentIaRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField()

    def _create_message(self, content: str, role: MessageRole) -> Message:
        user = self.context["request"].user

        conversation, _ = Conversation.objects.get_or_create(user=user)
        if not conversation.name:
            conversation.name = " ".join(content.split()[:5])
            conversation.save(update_fields=["name"])

        return Message.objects.create(
            content=content, conversation=conversation, role=role
        )

    def generate(self) -> tuple[Message, Message]:

        prompt = str(self.validated_data["prompt"])  # type: ignore
        prompt_msg = self._create_message(prompt, MessageRole.USER)

        username = self.context["request"].user.username
        logger.info(
            f"{username} sent a prompt to AgentIA: {prompt[:PROMPT_SPLITS]}...",
        )
        answer = GeminiApi.generate(prompt)
        answer_msg = self._create_message(answer, MessageRole.ASSISTANT)

        return answer_msg, prompt_msg


class AgentIaAnswerSerializer(serializers.Serializer):
    prompt = conversation.MessageSerializer()
    answer = conversation.MessageSerializer()
