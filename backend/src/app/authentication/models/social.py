from typing import ClassVar

from django.conf import settings
from django.db import models


class SocialProvider(models.TextChoices):
    """Providers defined for social account model"""

    GOOGLE = "google"
    GITHUB = "github"


class SocialAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="social_accounts",
    )
    provider = models.CharField(max_length=50, choices=SocialProvider.choices)
    provider_id = models.CharField(max_length=255)

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["provider", "provider_id"],
                name="unique_provider_account",
            ),
            models.UniqueConstraint(
                fields=["user", "provider"],
                name="unique_user_provider",
            ),
        ]
