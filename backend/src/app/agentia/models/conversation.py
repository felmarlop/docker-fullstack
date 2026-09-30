from django.conf import settings
from django.db import models

from app.agentia.models.choices import MessageRole
from app.core.models import BaseModel


class Conversation(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversation",
    )


class Message(BaseModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=50, choices=MessageRole.choices)
    content = models.TextField()
