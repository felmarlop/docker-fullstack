from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

from app.authentication.serializers.user import UserSerializer


class LoginSerializer(BaseTokenObtainPairSerializer):
    """
    Authenticate a user and return JWT tokens.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class LogoutSerializer(serializers.Serializer):
    """
    Logout the user by invalidating the refresh token.
    """

    refresh = serializers.CharField(write_only=True)

    def save(self):
        refresh = self.validated_data["refresh"]

        try:
            RefreshToken(refresh).blacklist()
        except TokenError as exc:
            raise serializers.ValidationError(
                {
                    "refresh": ["Invalid or expired refresh token."]
                }
            ) from exc
