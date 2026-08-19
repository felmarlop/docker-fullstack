from rest_framework import serializers

from app.authentication.constants import (
    RESERVED_PREFIXES,
    RESERVED_USERNAMES,
)


def validate_username(username: str) -> str:
    username = username.strip().lower()

    if not username:
        return username

    if username in RESERVED_USERNAMES:
        raise serializers.ValidationError("This username is reserved.")
    if any(username.startswith(prefix) for prefix in RESERVED_PREFIXES):
        raise serializers.ValidationError("This username is reserved.")

    return username
