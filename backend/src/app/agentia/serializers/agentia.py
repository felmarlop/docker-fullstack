import logging

from rest_framework import serializers

from app.agentia.api import api as GeminiApi

logger = logging.getLogger(__name__)


class AgentIaRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField()

    def generate(self) -> tuple[str, str]:
        user = self.context["request"].user
        prompt = str(self.validated_data["prompt"])  # type: ignore

        logger.info("%s sent a prompt to AgentIA", user.username)
        answer = GeminiApi.generate(prompt)  # type: ignore

        return answer, prompt


class AgentIaAnswerSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    answer = serializers.CharField()
