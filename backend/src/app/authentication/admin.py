from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from app.authentication.models.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Administration interface for the custom user model.
    """

    pass
