from django.db import models


class MessageRole(models.TextChoices):
    """Roles defined for message model"""

    ASSISTANT = "assistant"
    USER = "user"
