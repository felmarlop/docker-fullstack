from django.conf import settings
from django.urls import path

from app.core.views import email_preview

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path("preview/emails/", email_preview, name="email-preview"),
    ]
