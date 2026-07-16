from django.urls import path

from app.authentication.views import base, user

urlpatterns = [
    path("ping/", base.PingView.as_view(), name="ping"),
    path("users/me/", user.MeView.as_view(), name="users-me"),
]
