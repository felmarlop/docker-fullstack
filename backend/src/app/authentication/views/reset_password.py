from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.authentication.serializers import reset_password


class ForgotPasswordView(APIView):
    """
    Send instructions to reset password
    """

    def post(self, request: Request) -> Response:
        serializer = reset_password.ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordView(APIView):
    """
    Reset a user's password using a valid reset token.
    """

    def post(self, request: Request) -> Response:
        serializer = reset_password.ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
