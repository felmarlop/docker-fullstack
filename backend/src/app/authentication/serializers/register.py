from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from app.authentication.constants import (
    RESERVED_PREFIXES,
    RESERVED_USERNAMES,
)
from app.authentication.models import User
from app.authentication.services import send_activation_email


class RegisterSerializer(serializers.Serializer):
    """
    Register a new inactive user.
    """

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone = PhoneNumberField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_username(self, value: str) -> str:
        value = value.strip().lower()

        if value in RESERVED_USERNAMES:
            raise serializers.ValidationError("This username is reserved.")
        if any(value.startswith(prefix) for prefix in RESERVED_PREFIXES):
            raise serializers.ValidationError("This username is reserved.")

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value

    def validate_email(self, value: str) -> str:
        value = value.strip()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

    def validate_phone(self, value: PhoneNumber | None) -> PhoneNumber | None:
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists."
            )

        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)

        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data.get("phone"),
            password=validated_data["password"],
            is_active=False,
        )

    def save(self, **kwargs: Any) -> User:
        return super().save(**kwargs)


class ActivateAccountSerializer(serializers.Serializer):
    """
    Activate a user's account.
    """

    def _get_user_from_uidb64(self) -> User:
        uidb64 = self.context["uidb64"]

        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
            raise serializers.ValidationError(
                {
                    "uidb64": [
                        "Invalid activation link.",
                    ]
                }
            ) from exc
        return user

    def activate(self) -> User:
        user = self._get_user_from_uidb64()
        token = self.context["token"]

        if user.is_active:
            raise serializers.ValidationError(
                {
                    "user": [
                        "This account has already been activated.",
                    ]
                }
            )

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {
                    "token": [
                        "Invalid or expired activation link.",
                    ]
                }
            )

        user.is_active = True
        user.save(update_fields=["is_active"])

        return user


class ResendActivationEmailSerializer(serializers.Serializer):
    """
    Resend activation email.
    """

    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError(
                "No account is associated with this email address."
            ) from exc

        if self.user.is_active:
            raise serializers.ValidationError(
                "This account has already been activated."
            )

        return value

    def send_email(self) -> None:
        send_activation_email(self.user)
