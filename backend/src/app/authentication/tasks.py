from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_reset_password_email(email: str, url: str) -> None:
    msg = (
        "Hello,\n\n"
        "We received a request to reset your password.\n\n"
        "Click the following link to continue:\n\n"
        f"{url}\n\n"
        "If you didn't request this change, you can safely ignore this email."
    )
    email_msg = EmailMultiAlternatives(
        subject="Reset your password",
        body=msg,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    email_msg.send()
