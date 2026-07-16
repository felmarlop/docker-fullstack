
from rest_framework.serializers import ModelSerializer as BaseModelSerializer

from app.authentication.models import User


class UserSerializer(BaseModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
        )
