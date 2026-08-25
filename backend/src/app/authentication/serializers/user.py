from rest_framework import serializers
from rest_framework.serializers import ModelSerializer as BaseModelSerializer

from app.authentication.models import User


class UserSerializer(BaseModelSerializer):
    """
    Serializer for the User model.
    """

    has_usable_password = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

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
            "has_usable_password",
            "avatar_url",
        )

    def get_has_usable_password(self, obj: User) -> bool:
        return obj.has_usable_password()

    def get_avatar_url(self, obj: User) -> str | None:
        if not obj.avatar:
            return None

        request = self.context.get("request")
        url = obj.avatar.url

        if request:
            return request.build_absolute_uri(url)
        return url
