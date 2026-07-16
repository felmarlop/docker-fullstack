from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

from app.authentication.serializers.user import UserSerializer


class LoginSerializer(BaseTokenObtainPairSerializer):
    """
    Authenticate a user and return JWT tokens.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data
