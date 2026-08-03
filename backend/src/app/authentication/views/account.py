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
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
)

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
        logger.info(f"User {username} authenticated successfully.")
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
