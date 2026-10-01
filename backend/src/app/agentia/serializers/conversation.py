from django.shortcuts import get_object_or_404
from rest_framework import serializers

from app.agentia.models import Conversation, Message


class MinimumConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = (
            "name",
            "updated_at",
        )


class ConversationSerializer(MinimumConversationSerializer):
    class Meta(MinimumConversationSerializer.Meta):
        fields = (
            *MinimumConversationSerializer.Meta.fields,
            "id",
            "user",
            "created_at",
        )


class MinimumMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "role",
            "content",
            "conversation",
        )


class MessageSerializer(MinimumMessageSerializer):
    class Meta(MinimumMessageSerializer.Meta):
        fields = (
            *MinimumMessageSerializer.Meta.fields,
            "id",
            "updated_at",
            "created_at",
        )


class DeleteConversationSerializer(serializers.Serializer):
    def delete(self, conversation_id: int) -> None:
        user = self.context["request"].user
        conversation = get_object_or_404(Conversation, id=conversation_id, user=user)
        conversation.delete()
