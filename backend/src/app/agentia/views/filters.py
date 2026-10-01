import django_filters

from app.agentia.models import Message


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ["conversation", "role"]  # noqa
