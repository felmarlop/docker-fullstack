import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from app.subscription.models import Subscription
from app.subscription.views import subscription as s_views

logger = logging.getLogger(__name__)


@shared_task
def send_active_subscription_email(subscription_id: int) -> None:
    """
    Send an email to the user when a subscription is active.
    """

    subscription = Subscription.objects.select_related("stripe_customer__user").get(
        id=subscription_id
    )
    plan_title = s_views.STRIPE_PLANS[subscription.plan]["title"]
    user = subscription.stripe_customer.user

    html_content = render_to_string(
        "emails/subscription_activation.html",
        {
            "user": user,
            "plan_title": plan_title,
        },
    )

    msg = (
        "Congratulations!\n\n"
        "Your subscription is now active, and your new benefits are ready to enjoy.\n\n"
        f"Your plan: {plan_title.upper()}.\n\n"
        "Thank you for upgrading!"
    )

    try:
        email_msg = EmailMultiAlternatives(
            subject=f"Your {plan_title} subscription is now active",
            body=msg,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()
    except Exception:
        logger.exception(f"Failed to send active subscription email to {user.email}.")
        raise
