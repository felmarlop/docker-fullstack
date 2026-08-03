from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from app.authentication.models import User
from app.authentication.services import send_reset_password_email

token_generator = PasswordResetTokenGenerator()


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Send instructions to reset password
    """

    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError(
                {
                    "email": [
                        "No account is associated with this email address.",
                    ]
                }
            ) from exc
        return value

    def send_email(self) -> None:
        send_reset_password_email(self.user)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset a user's password using a valid reset token.
    """

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uid"]))
            self.user = User.objects.get(pk=uid)
        except Exception as exc:
            raise serializers.ValidationError(
                {
                    "uid": [
                        "Invalid password reset link.",
                    ],
                }
            ) from exc

        token = attrs["token"]

        if not token_generator.check_token(self.user, token):
            raise serializers.ValidationError(
                {
                    "token": [
                        "The password reset link is invalid or has expired.",
                    ],
                }
            )

        try:
            validate_password(attrs["new_password"], self.user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                {
                    "new_password": exc.messages,
                }
            ) from exc

        return attrs

    def save(self, **kwargs: Any) -> User:  # noqa: ARG002
        self.user.set_password(self.validated_data["new_password"])  # type: ignore
        self.user.save(update_fields=["password"])
        return self.user
