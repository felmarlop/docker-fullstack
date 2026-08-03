import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.authentication.serializers.register import (
    ActivateAccountSerializer,
    RegisterSerializer,
    ResendActivationEmailSerializer,
)
from app.authentication.services import send_activation_email

logger = logging.getLogger(__name__)


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


class ResendActivationEmailView(APIView):
    """
    Resend activation email
    """

    serializer_class = ResendActivationEmailSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.send_email()  # type: ignore

        email = serializer.validated_data["email"]  # type: ignore
        logger.info(f"Activation email requested for {email}.")

        return Response(status=status.HTTP_204_NO_CONTENT)
