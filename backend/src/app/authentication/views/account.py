import logging
from typing import Any

from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView as BaseTokenRefreshView,
)

from app.authentication.serializers.account import (
    ChangeEmailSerializer,
    ChangePasswordSerializer,
    DeleteAccountSerializer,
    LoginSerializer,
    LogoutSerializer,
    ResendEmailVerificationSerializer,
    VerifyEmailSerializer,
)
from app.authentication.serializers.user import UserSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    summary="User login",
    description="Authenticate a user and return JWT access and refresh tokens",
    request=LoginSerializer,
    tags=["Authentication"],
    responses={200: LoginSerializer},
    examples=[
        OpenApiExample(
            "Login request",
            value={
                "username": "fmartin",
                "password": "myStrongPassword123",
            },
            request_only=True,
        ),
    ],
)
class LoginView(BaseTokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        username = request.data.get("username")  # type: ignore
        response = super().post(request, *args, **kwargs)
        logger.info(f"{username} authenticated successfully.")
        return response


@extend_schema(
    summary="Refresh access token",
    description="Generate a new access token using a valid refresh token",
    request=TokenRefreshSerializer,
    tags=["Authentication"],
    responses={200: TokenRefreshSerializer},
    examples=[
        OpenApiExample(
            "Refresh token",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIs...",
            },
            request_only=True,
        ),
    ],
)
class RefreshTokenView(BaseTokenRefreshView):
    serializer_class = TokenRefreshSerializer
    pass


@extend_schema(
    summary="Change password",
    description="Change the authenticated user's password",
    request=ChangePasswordSerializer,
    tags=["Password"],
    examples=[
        OpenApiExample(
            "Change password",
            value={
                "current_password": "myCurrentPassword123",
                "new_password": "myNewPassword123",
            },
            request_only=True,
        ),
    ],
)
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info(f"Password changed successfully for user {user.username}.")  # type: ignore
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Change Email",
    description="Change the authenticated user's email",
    request=ChangeEmailSerializer,
    tags=["Email"],
    examples=[
        OpenApiExample(
            "Change email",
            value={
                "email": "fmartin@example.com",
            },
            request_only=True,
        ),
    ],
)
class ChangeEmailView(APIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info(f"Email change requested for user {user.username}.")  # type: ignore
        return Response(UserSerializer(user).data)


@extend_schema(
    summary="Verify email",
    description="Verify a user's email using a user ID and activation token.",
    request=VerifyEmailSerializer,
    tags=["Email"],
)
class VerifyEmailView(APIView):
    serializer_class = VerifyEmailSerializer

    def get(self, request: Request, uidb64: str, token: str) -> Response:  # noqa: ARG002
        serializer = self.serializer_class(
            context={
                "uidb64": uidb64,
                "token": token,
            }
        )

        user = serializer.verify()  # type: ignore
        logger.info(f"Email verified successfully for user {user.username}.")
        return Response(UserSerializer(user).data)


@extend_schema(
    summary="Resend email verification",
    description="Resend the email verification if user's pending email exists.",
    request=ResendEmailVerificationSerializer,
    tags=["Email"],
    examples=[
        OpenApiExample(
            "Resend email verification",
            value={
                "email": "fmartin@example.com",
            },
            request_only=True,
        ),
    ],
)
class ResendEmailVerificationView(APIView):
    """
    Resend email verification
    """

    serializer_class = ResendEmailVerificationSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.send_email()  # type: ignore

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Logout user",
    description="Invalidate a refresh token.",
    request=LogoutSerializer,
    tags=["Authentication"],
    examples=[
        OpenApiExample(
            "Logout request",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIs...",
            },
            request_only=True,
        ),
    ],
)
class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"User {request.user.username} logged out.")
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Delete account",
    description="Permanently delete the authenticated user's account.",
    request=DeleteAccountSerializer,
    tags=["Authentication"],
    examples=[
        OpenApiExample(
            "Delete request",
            value={
                "confirmation": "DELETE",
                "refresh": "eyJhbGciOiJIUzI1NiIs...",
                "password": "myNewPassword123",
            },
            request_only=True,
        ),
    ],
)
class DeleteAccountView(APIView):
    serializer_class = DeleteAccountSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        serializer.delete()  # type: ignore

        logger.info(f"Account deleted: {request.user.username}.")
        return Response(status=status.HTTP_204_NO_CONTENT)
