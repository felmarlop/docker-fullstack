from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from app.authentication.tasks import send_reset_password_email

token_generator = PasswordResetTokenGenerator()

User = get_user_model()


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

    def save(self, **kwargs: Any) -> None:  # noqa: ARG002
        email = self.validated_data["email"]  # type: ignore

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)

        url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
        send_reset_password_email.delay(email, url)  # pyright: ignore[reportFunctionMemberAccess]


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

    def save(self, **kwargs: Any) -> None:  # noqa: ARG002
        self.user.set_password(self.validated_data["new_password"])  # type: ignore
        self.user.save(update_fields=["password"])
