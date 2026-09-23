import django_filters

from app.authentication.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ["is_staff", "is_superuser"]  # noqa
