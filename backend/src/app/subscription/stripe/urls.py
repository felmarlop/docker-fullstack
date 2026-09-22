from django.urls import path

from app.subscription.stripe import webhook

urlpatterns = [
    path(
        "stripe/webhook/",
        webhook.StripWebhookView.as_view(),
        name="sync-subscription",
    ),
]
