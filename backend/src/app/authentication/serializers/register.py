import logging
from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from app.authentication import utils, validators
from app.authentication.models import User
from app.authentication.services import send_account_activation

logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.Serializer):
    """
    Register a new inactive user.
    """

    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()
    phone = PhoneNumberField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def _generate_username(self, email: str) -> str:
        base = email.split("@")[0].strip().lower() or "user"

        username = base
        counter = 2

        while User.objects.filter(username=username).exists():
            username = f"{base}{counter}"
            counter += 1

        return username

    def validate_username(self, value: str) -> str:
        value = validators.validate_username(value)

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
        if not value:
            return None

        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists."
            )

        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)

        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        email = validated_data["email"]
        username = validated_data.get("username") or self._generate_username(email)

        return User.objects.create_user(
            username=username,
            email=email,
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

    def activate(self) -> User:
        user = utils.get_user_from_uidb64(self.context["uidb64"])
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

    def send_email(self) -> None:
        email = self.validated_data["email"]  # type: ignore
        user = User.objects.filter(email__iexact=email).first()

        if user and not user.is_active:
            send_account_activation(user)
        elif user and user.is_active:
            logger.warning(
                f"Activation email: Account already activated for user {user.username}."
            )
        else:
            logger.warning(f"Activation email: No user found with email {email}.")
