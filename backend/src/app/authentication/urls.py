from django.urls import path

from app.authentication.views import account, base, user

urlpatterns = [
    path("ping/", base.PingView.as_view(), name="ping"),
    path("users/me/", user.MeView.as_view(), name="users-me"),

    path("auth/login/", account.LoginView.as_view(), name="account-login"),
    path( "auth/refresh/", account.RefreshTokenView.as_view(), name="account-refresh"),
]
