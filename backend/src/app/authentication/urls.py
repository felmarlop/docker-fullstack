from django.urls import path

from app.authentication.views import (
    account,
    register,
    reset_password,
    social,
    user,
)

urlpatterns = [
    path("users/me/", user.MeView.as_view(), name="users-me"),
    path("auth/login/", account.LoginView.as_view(), name="login"),
    path("auth/register/", register.RegisterView.as_view(), name="register"),
    path("auth/refresh/", account.RefreshTokenView.as_view(), name="token-refresh"),
    path("oauth/google/", social.GoogleView.as_view(), name="auth-google"),
    path("oauth/github/", social.GithubView.as_view(), name="auth-github"),
    path(
        "auth/activate/<uidb64>/<token>/",
        register.ActivateAccountView.as_view(),
        name="activate-account",
    ),
    path(
        "auth/activate/resend/",
        register.ResendActivationEmailView.as_view(),
        name="resend-activation-email",
    ),
    path(
        "auth/change-avatar/", account.ChangeAvatarView.as_view(), name="change-avatar"
    ),
    path(
        "auth/delete-avatar/", account.DeleteAvatarView.as_view(), name="delete-avatar"
    ),
    path("auth/change-email/", account.ChangeEmailView.as_view(), name="change-email"),
    path(
        "auth/verify-email/<uidb64>/<token>/",
        account.VerifyEmailView.as_view(),
        name="verify-email",
    ),
    path(
        "auth/verify-email/resend/",
        account.ResendEmailVerificationView.as_view(),
        name="resend-email-verification",
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
    path("auth/logout/", account.LogoutView.as_view(), name="logout"),
    path(
        "auth/delete-account/",
        account.DeleteAccountView.as_view(),
        name="delete-account",
    ),
]
