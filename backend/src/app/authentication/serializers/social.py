import logging
from typing import Any

from django.conf import settings
from django.db import transaction
from google.auth.transport import requests
from google.oauth2 import id_token as google_id_token
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.authentication import utils
from app.authentication.models import SocialAccount, SocialProvider, User
from app.authentication.serializers.user import UserSerializer

logger = logging.getLogger(__name__)


class GoogleSerializer(serializers.Serializer):
    """
    Authenticate a user with Google.
    """

    id_token = serializers.CharField(write_only=True)

    def _validate_google_token(self, value: str) -> dict[str, Any]:
        try:
            id_info = google_id_token.verify_oauth2_token(
                value,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
        except ValueError as exc:
            raise serializers.ValidationError("Invalid Google ID token.") from exc

        return {
            "provider_id": id_info["sub"],
            "email": id_info["email"],
            "email_verified": id_info["email_verified"],
        }

    def validate_id_token(self, value: str) -> str:
        self.google_data = self._validate_google_token(value)
        if not self.google_data["email_verified"]:
            raise serializers.ValidationError(
                "The Google account email is not verified."
            )
        return value

    @transaction.atomic
    def save(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ARG002
        provider_id = self.google_data["provider_id"]
        email = self.google_data["email"]

        social_qs = SocialAccount.objects.select_related("user").filter(
            provider=SocialProvider.GOOGLE,
            provider_id=provider_id,
        )
        if social_account := social_qs.first():
            user = social_account.user
            user = utils.activate_user(user)
            logger.info(f"{user.username} authenticated successfully with Google.")  # type: ignore
        else:
            user = User.objects.filter(email__iexact=email).first()
            if user is None:
                user = User.objects.create(
                    username=utils.generate_username_from_email(email), email=email
                )

                user.set_unusable_password()
                user.save(update_fields=["password"])
            else:
                user = utils.activate_user(user)

            social_account = SocialAccount.objects.filter(
                user=user,
                provider=SocialProvider.GOOGLE,
            ).first()
            if social_account:
                social_account.provider_id = provider_id
                social_account.save(update_fields=["provider_id"])
            else:
                SocialAccount.objects.create(
                    user=user,
                    provider=SocialProvider.GOOGLE,
                    provider_id=provider_id,
                )

            logger.info(f"Account created for {user.username} using Google.")  # type: ignore

        refresh = TokenObtainPairSerializer.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),  # type: ignore
            "user": UserSerializer(user).data,
        }
