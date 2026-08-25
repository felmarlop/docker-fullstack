from django.core.exceptions import ValidationError
from django.core.files import File

from app.authentication.constants import (
    RESERVED_PREFIXES,
    RESERVED_USERNAMES,
)


def validate_username(username: str) -> str:
    username = username.strip().lower()

    if not username:
        return username

    if username in RESERVED_USERNAMES:
        raise ValidationError("This username is reserved.")
    if any(username.startswith(prefix) for prefix in RESERVED_PREFIXES):
        raise ValidationError("This username is reserved.")

    return username


def validate_avatar_size(value: File) -> None:
    max_size = 2 * 1024 * 1024  # 2 MB
    if value.size > max_size:
        raise ValidationError("Avatar image cannot exceed 2 MB.")
