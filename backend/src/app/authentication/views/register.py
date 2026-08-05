import logging

from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.authentication.serializers.account import LoginSerializer
from app.authentication.serializers.register import (
    ActivateAccountSerializer,
    RegisterSerializer,
    ResendActivationEmailSerializer,
)
from app.authentication.services import send_activation_email

logger = logging.getLogger(__name__)


@extend_schema(
    summary="Register user",
    description="Register a new inactive user and send an activation email",
    request=RegisterSerializer,
    tags=["Registration"],
    responses={200: LoginSerializer},
    examples=[
        OpenApiExample(
            "Register request",
            value={
                "username": "fmartin",
                "email": "fmartin@example.com",
                "phone": "+34600111222",
                "password": "myStrongPassword123",
            },
            request_only=True,
        ),
    ],
)
class RegisterView(APIView):
    """
    Register a new inactive user
    """

    serializer_class = RegisterSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        send_activation_email(user)  # type: ignore
        logger.info(f"Inactive account created for {user.username}.")  # type: ignore

        return Response(
            {
                "detail": "Your account has been created. Please check your email.",
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    summary="Activate account",
    description="Activate a user account using a user ID and activation token.",
    request=ActivateAccountSerializer,
    tags=["Registration"],
)
class ActivateAccountView(APIView):
    """
    Activate a user's account.
    """

    serializer_class = ActivateAccountSerializer

    def get(self, request: Request, uidb64: str, token: str) -> Response:  # noqa: ARG002
        serializer = self.serializer_class(
            context={
                "uidb64": uidb64,
                "token": token,
            }
        )

        user = serializer.activate()  # type: ignore
        logger.info(f"Account activated for {user.username}.")  # type: ignore

        return Response(
            {
                "detail": "Your account has been successfully activated.",
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    summary="Resend activation email",
    description="Resend the activation email if the account exists and it's inactive.",
    request=ResendActivationEmailSerializer,
    tags=["Registration"],
    examples=[
        OpenApiExample(
            "Resend activation email request",
            value={
                "email": "fmartin@example.com",
            },
            request_only=True,
        ),
    ],
)
class ResendActivationEmailView(APIView):
    """
    Resend activation email
    """

    serializer_class = ResendActivationEmailSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.send_email()  # type: ignore

        return Response(status=status.HTTP_204_NO_CONTENT)
