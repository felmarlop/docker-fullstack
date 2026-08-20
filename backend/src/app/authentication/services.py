from django.conf import settings
from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator,
)

from app.authentication import tasks, tokens
from app.authentication.models import User

reset_token_generator = PasswordResetTokenGenerator()


def send_account_activation(user: User) -> None:
    uidb64, token = tokens.generate_activation_token(user)
    url = f"{settings.FRONTEND_URL}/activate/{uidb64}/{token}/"
    tasks.send_activation_email.delay(user.email, url)  # pyright: ignore[reportFunctionMemberAccess]


def send_email_verification(user: User) -> None:
    uidb64, token = tokens.generate_email_verification_token(user)
    url = f"{settings.FRONTEND_URL}/verify/email/{uidb64}/{token}"
    tasks.send_email_verification_email.delay(user.email, url)  # pyright: ignore[reportFunctionMemberAccess]


def send_password_reset(user: User) -> None:
    uidb64, token = tokens.generate_reset_password_token(user)
    url = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}"
    tasks.send_password_reset_email.delay(user.email, url)  # pyright: ignore[reportFunctionMemberAccess]
