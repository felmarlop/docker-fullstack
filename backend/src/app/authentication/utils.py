from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from app.authentication.models import User


def get_user_from_uidb64(uidb64: str) -> User:
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
        raise serializers.ValidationError(
            {
                "uidb64": [
                    "Invalid user id.",
                ]
            }
        ) from exc

    return user
