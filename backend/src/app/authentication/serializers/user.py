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
            "first_name",
            "last_name",
            "email",
            "pending_email",
            "is_staff",
            "is_superuser",
        )
