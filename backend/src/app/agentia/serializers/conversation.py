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
            "updated_at",
        )


class MessageSerializer(MinimumMessageSerializer):
    class Meta(MinimumMessageSerializer.Meta):
        fields = (
            *MinimumMessageSerializer.Meta.fields,
            "id",
            "conversation",
            "created_at",
        )
