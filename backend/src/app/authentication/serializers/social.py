import logging
from typing import Any

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from google.auth.transport.requests import Request
from google.oauth2 import id_token as google_id_token
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.authentication import utils
from app.authentication.models import SocialAccount, SocialProvider, User

logger = logging.getLogger(__name__)


class BaseSocialSerializer(serializers.Serializer):
    def _get_or_create_user(
        self,
        provider: SocialProvider,
        data: dict,
    ) -> User:
        provider_id = data["provider_id"]
        email = data["email"]

        social_account = (
            SocialAccount.objects.select_related("user")
            .filter(
                provider=provider,
                provider_id=provider_id,
            )
            .first()
        )

        if social_account:
            user = utils.activate_user(social_account.user)
        else:
            user = User.objects.filter(email__iexact=email).first()
            if user is None:
                user = User.objects.create(
                    username=utils.generate_username_from_email(email),
                    email=email,
                )
                user.set_unusable_password()
                user.save(update_fields=["password"])
                logger.info(f"Account created for {user.username} using {provider}.")
            else:
                user = utils.activate_user(user)

            SocialAccount.objects.update_or_create(
                user=user,
                provider=provider,
                defaults={"provider_id": provider_id},
            )

        if data.get("avatar_url") and not user.avatar:
            self._set_avatar_from_url(user, data["avatar_url"])

        return user

    def _get_tokens(self, user: User) -> dict[str, Any]:
        refresh = TokenObtainPairSerializer.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),  # type: ignore
            "user": utils.serialize_user(user, self.context.get("request")),
        }

    def _set_avatar_from_url(self, user: User, avatar_url: str) -> None:
        try:
            response = requests.get(avatar_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.warning(f"Unable to download avatar for {user.username}: {exc}")
            return

        filename = f"{user.username}_avatar.jpg"
        user.avatar.save(filename, ContentFile(response.content), save=True)
        user.save(update_fields=["avatar"])

class GoogleSerializer(BaseSocialSerializer):
    """
    Authenticate a user with Google.
    """

    id_token = serializers.CharField(write_only=True)

    def _validate_google_token(self, value: str) -> dict[str, Any]:
        try:
            id_info = google_id_token.verify_oauth2_token(
                value,
                Request(),
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
        user = self._get_or_create_user(SocialProvider.GOOGLE, self.google_data)
        tokens = self._get_tokens(user)

        logger.info(f"{user.username} authenticated successfully with Google.")  # type: ignore
        return tokens


class GithubSerializer(BaseSocialSerializer):
    """
    Authenticate a user with GitHub.
    """

    code = serializers.CharField(write_only=True)

    def _get_github_email(self, access_token: str) -> str | None:
        try:
            response = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github+json",
                },
                timeout=10,
            )
            emails = response.json()
        except requests.RequestException as exc:
            raise serializers.ValidationError(
                "Unable to retrieve GitHub account email."
            ) from exc

        for email_data in emails:
            if email_data.get("primary") and email_data.get("verified"):
                return email_data["email"]
        return None

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        try:
            response = requests.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_SECRET_KEY,
                    "code": attrs["code"],
                },
                headers={
                    "Accept": "application/json",
                },
                timeout=10,
            )
            token_data = response.json()
        except requests.RequestException as exc:
            raise serializers.ValidationError(
                "We could not log you in with GitHub. Please try again later."
            ) from exc

        access_token = token_data.get("access_token")

        if not access_token:
            raise serializers.ValidationError("Invalid GitHub authorization code.")

        try:
            response = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github+json",
                },
                timeout=10,
            )
            github_user = response.json()
        except requests.RequestException as exc:
            raise serializers.ValidationError(
                "Unable to retrieve GitHub user information."
            ) from exc

        email = github_user.get("email")
        if not email:
            email = self._get_github_email(access_token)

        if not email:
            raise serializers.ValidationError(
                "Unable to retrieve the GitHub account email."
            )

        self.github_data = {
            "provider_id": str(github_user["id"]),
            "email": email,
            "avatar_url": github_user.get("avatar_url"),
        }

        return attrs

    @transaction.atomic
    def save(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ARG002
        user = self._get_or_create_user(SocialProvider.GITHUB, self.github_data)
        tokens = self._get_tokens(user)

        logger.info(f"{user.username} authenticated successfully with GitHub.")  # type: ignore
        return tokens
