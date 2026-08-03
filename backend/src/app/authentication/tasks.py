import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


@shared_task
def send_activation_email(email: str, url: str) -> None:
    """
    Send an account activation email.
    """
    msg = (
        "Hello,\n\n"
        "Thank you for registering.\n\n"
        "Please click the following link to activate your account:\n\n"
        f"{url}\n\n"
        "If you didn't create this account, you can safely ignore this email."
    )

    try:
        email_msg = EmailMultiAlternatives(
            subject="Activate your account",
            body=msg,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_msg.send()
    except Exception:
        logger.exception(f"Failed to send activation email to {email}.")
        raise


@shared_task
def send_reset_password_email(email: str, url: str) -> None:
    """
    Send a password reset email.
    """
    msg = (
        "Hello,\n\n"
        "We received a request to reset your password.\n\n"
        "Click the following link to continue:\n\n"
        f"{url}\n\n"
        "If you didn't request this change, you can safely ignore this email."
    )

    try:
        email_msg = EmailMultiAlternatives(
            subject="Reset your password",
            body=msg,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_msg.send()
    except Exception:
        logger.exception(f"Failed to send password reset email to {email}.")
        raise


@shared_task
def heartbeat() -> None:
    """
    Simple periodic task used to verify that Celery Beat is running.
    """
    logger.info("Heartbeat task executed successfully.")
