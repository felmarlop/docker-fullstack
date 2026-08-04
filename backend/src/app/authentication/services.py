from django.conf import settings
from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator,
    default_token_generator,
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from app.authentication import tasks
from app.authentication.models import User

reset_token_generator = PasswordResetTokenGenerator()


def send_activation_email(user: User) -> None:
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    url = f"{settings.FRONTEND_URL}/activate/{uidb64}/{token}/"
    tasks.send_activation_email.delay(user.email, url)  # pyright: ignore[reportFunctionMemberAccess]


def send_reset_password_email(user: User) -> None:
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = reset_token_generator.make_token(user)

    url = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}"
    tasks.send_reset_password_email.delay(user.email, url)  # pyright: ignore[reportFunctionMemberAccess]
