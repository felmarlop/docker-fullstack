from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from app.authentication.models import User
from app.authentication.services import send_password_reset

token_generator = PasswordResetTokenGenerator()


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Send instructions to reset password
    """

    email = serializers.EmailField()

    def send_email(self) -> None:
        email = self.validated_data["email"]  # type: ignore
        user = User.objects.filter(email__iexact=email).first()

        if user and user.is_active:
            send_password_reset(user)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset a user's password using a valid reset token.
    """

    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uidb64"]))
            self.user = User.objects.get(pk=uid)
        except Exception as exc:
            raise serializers.ValidationError(
                {
                    "uidb64": [
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
                    "password": exc.messages,
                }
            ) from exc

        return attrs

    def save(self, **kwargs: Any) -> User:  # noqa: ARG002
        self.user.set_password(self.validated_data["new_password"])  # type: ignore
        self.user.save(update_fields=["password"])
        return self.user
