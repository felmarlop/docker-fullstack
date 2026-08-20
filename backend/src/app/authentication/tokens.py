from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator,
    default_token_generator,
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from app.authentication.models import User


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: int) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
        return (
            f"{user.pk}{user.pending_email}{user.password}{user.last_login}{timestamp}"
        )


reset_token_generator = PasswordResetTokenGenerator()
email_verification_token_generator = EmailVerificationTokenGenerator()


def generate_activation_token(user: User) -> tuple[str, str]:
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    return uidb64, token


def generate_email_verification_token(user: User) -> tuple[str, str]:
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token_generator.make_token(user)

    return uidb64, token


def generate_reset_password_token(user: User) -> tuple[str, str]:
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = reset_token_generator.make_token(user)

    return uidb64, token
