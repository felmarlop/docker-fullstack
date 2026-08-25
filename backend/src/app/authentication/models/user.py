from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from app.authentication import validators


class User(AbstractUser):
    """
    Custom user model.
    """

    pending_email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
    )

    phone = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        help_text="Phone number in E.164 format.",
    )

    is_phone_verified = models.BooleanField(default=False)

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp"],
            ),
            validators.validate_avatar_size,
        ],
    )
