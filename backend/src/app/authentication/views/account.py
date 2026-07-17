from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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


class LoginView(BaseTokenObtainPairView):
    """
    Authenticate a user and return JWT tokens and user information
    """

    serializer_class = LoginSerializer


class RefreshTokenView(BaseTokenRefreshView):
    """
    Refresh an access token.
    """

    pass


class ChangePasswordView(APIView):
    """
    Change the authenticated user's password.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):
    """
    Logout the user by invalidating the refresh token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
