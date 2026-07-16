from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView as BaseTokenRefreshView,
)

from app.authentication.serializers.account import LoginSerializer


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
