from django.contrib.auth.password_validation import validate_password
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


class ChangePasswordSerializer(serializers.Serializer):
    """
    Change the authenticated user's password.
    """

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user

        if user.check_password(attrs["new_password"]):
            raise serializers.ValidationError(
                {
                    "new_password": [
                        "The new password must be different from the current password.",
                    ],
                }
            )
        elif not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError(
                {
                    "current_password": ["Current password is incorrect."],
                }
            )

        validate_password(attrs["new_password"], user)
        return attrs

    def save(self):
        user = self.context["request"].user
        pwd = self.validated_data["new_password"]
        user.set_password(pwd)
        user.save(update_fields=["password"])


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
                    "refresh": ["Invalid or expired refresh token."],
                }
            ) from exc
