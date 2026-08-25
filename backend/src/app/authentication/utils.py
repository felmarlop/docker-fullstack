from typing import Any

from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.request import Request

from app.authentication.models import User
from app.authentication.serializers.user import UserSerializer


def generate_username_from_email(email: str) -> str:
    base = email.split("@")[0].strip().lower() or "user"

    username = base
    counter = 2
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1

    return username


def activate_user(user: User) -> User:
    user.is_active = True
    user.save(update_fields=["is_active"])
    return user


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


def serialize_user(user: User, request: Request | None) -> dict[str, Any]:
    return UserSerializer(
        user,
        context={"request": request},
    ).data
