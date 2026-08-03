from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """
    Custom user model.
    """

    phone = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        help_text="Phone number in E.164 format.",
    )

    is_phone_verified = models.BooleanField(default=False)
