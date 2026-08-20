import logging
from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

from app.authentication import utils, validators
from app.authentication.exceptions import AccountNotActivated
from app.authentication.models import User
from app.authentication.serializers.user import UserSerializer
from app.authentication.services import send_email_verification
from app.authentication.tokens import email_verification_token_generator

logger = logging.getLogger(__name__)


class LoginSerializer(BaseTokenObtainPairSerializer):
    """
    Authenticate a user and return JWT tokens.
    """

    username = serializers.CharField(write_only=True, required=False)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        username = attrs["username"].strip()

        user = (
            User.objects.filter(username__iexact=username).first()
            or User.objects.filter(email__iexact=username).first()
        )

        if user:
            if not user.is_active:
                raise AccountNotActivated(
                    "Please activate your account before signing in."
                )
            attrs["username"] = user.username

        data = super().validate(attrs)

        return {
            **data,
            "user": UserSerializer(self.user).data,
        }


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )

    def validate_username(self, value: str) -> str:
        value = validators.validate_username(value)

        queryset = User.objects.filter(username=value)
        if self.instance:
            queryset = queryset.exclude(username=self.instance.username)

        if queryset.exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value


class ChangeEmailSerializer(serializers.Serializer):
    """
    Change the authenticated user's email.
    """

    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        user = self.context["request"].user
        value = value.strip()

        if value.lower() == user.email.lower():
            raise serializers.ValidationError(
                "The new email must be different from the current email."
            )

        queryset = User.objects.exclude(pk=user.pk)

        if queryset.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        if queryset.filter(pending_email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this pending email already exists."
            )

        return value

    def save(self, **kwargs: Any) -> User:  # noqa: ARG002
        user = self.context["request"].user

        user.pending_email = self.validated_data["email"]  # type: ignore
        user.save(update_fields=["pending_email"])

        send_email_verification(user)

        return user


class VerifyEmailSerializer(serializers.Serializer):
    """
    Verify a pending email address.
    """

    def verify(self) -> User:
        user = utils.get_user_from_uidb64(self.context["uidb64"])
        token = self.context["token"]

        if not user.pending_email:
            raise serializers.ValidationError(
                {
                    "email": [
                        "There is no pending email to verify.",
                    ]
                }
            )

        if not email_verification_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {
                    "token": [
                        "Invalid or expired verification link.",
                    ]
                }
            )

        user.email = user.pending_email
        user.pending_email = None
        user.save(update_fields=["email", "pending_email"])

        return user


class ResendEmailVerificationSerializer(serializers.Serializer):
    """
    Resend email verification.
    """

    email = serializers.EmailField()

    def send_email(self) -> None:
        email = self.validated_data["email"]  # type: ignore
        user = User.objects.filter(pending_email__iexact=email).first()

        if user:
            send_email_verification(user)
        else:
            logger.warning(
                f"Email verification: No user found with pending email {email}."
            )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Change the authenticated user's password.
    """

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        user = self.context["request"].user

        if user.check_password(attrs["new_password"]):
            raise serializers.ValidationError(
                {
                    "new_password": [
                        "The new password must be different from the current password.",
                    ],
                }
            )

        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError(
                {
                    "current_password": ["Current password is incorrect."],
                }
            )

        try:
            validate_password(attrs["new_password"], user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                {
                    "new_password": exc.messages,
                }
            ) from exc

        return attrs

    def save(self, **kwargs: Any) -> User:  # noqa: ARG002
        user = self.context["request"].user
        pwd = self.validated_data["new_password"]  # type: ignore
        user.set_password(pwd)
        user.save(update_fields=["password"])
        return user


class LogoutSerializer(serializers.Serializer):
    """
    Logout the user by invalidating the refresh token.
    """

    refresh = serializers.CharField(write_only=True)

    def save(self, **kwargs: Any) -> None:  # noqa: ARG002
        refresh = self.validated_data["refresh"]  # type: ignore

        try:
            RefreshToken(refresh).blacklist()
        except TokenError as exc:
            raise serializers.ValidationError(
                {
                    "refresh": ["Invalid or expired refresh token."],
                }
            ) from exc
