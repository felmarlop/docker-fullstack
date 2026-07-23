import logging

from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.authentication.serializers.reset_password import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

logger = logging.getLogger(__name__)


@extend_schema(
    auth=[],
    summary="Request password reset",
    description="Send instructions to reset the user's password",
    request=ForgotPasswordSerializer,
    tags=["Password"],
    examples=[
        OpenApiExample(
            "Forgot password",
            value={
                "email": "fmartin@test.com",
            },
            request_only=True,
        ),
    ],
)
class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request: Request) -> Response:
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data["email"]  # type: ignore
        logger.info(f"Password reset requested for {email}.")
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    auth=[],
    summary="Reset password",
    description="Reset the user's password using a valid reset token",
    request=ResetPasswordSerializer,
    tags=["Password"],
    examples=[
        OpenApiExample(
            "Reset password",
            value={
                "uid": "Mg",
                "token": "dc4b1z-4e00cdd129eb33400327e67d3c426ca7",
                "new_password": "myNewPassword123",
            },
            request_only=True,
        ),
    ],
)
class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request: Request) -> Response:
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Password reset completed for user {serializer.user.username}.")  # type: ignore
        return Response(status=status.HTTP_204_NO_CONTENT)
