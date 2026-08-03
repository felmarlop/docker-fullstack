from django.urls import path

from app.authentication.views import account, base, register, reset_password, user

urlpatterns = [
    path("ping/", base.PingView.as_view(), name="ping"),
    path("users/me/", user.MeView.as_view(), name="users-me"),
    path("auth/login/", account.LoginView.as_view(), name="login"),
    path("auth/logout/", account.LogoutView.as_view(), name="logout"),
    path("auth/refresh/", account.RefreshTokenView.as_view(), name="token-refresh"),
    path("register/", register.RegisterView.as_view(), name="register"),
    path(
        "activate/<uidb64>/<token>/",
        register.ActivateAccountView.as_view(),
        name="activate-account",
    ),
    path(
        "activate/resend/",
        register.ResendActivationEmailView.as_view(),
        name="resend-activation-email",
    ),
    path(
        "auth/change-password/",
        account.ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "auth/forgot-password/",
        reset_password.ForgotPasswordView.as_view(),
        name="forgot-password",
    ),
    path(
        "auth/reset-password/",
        reset_password.ResetPasswordView.as_view(),
        name="reset-password",
    ),
]
