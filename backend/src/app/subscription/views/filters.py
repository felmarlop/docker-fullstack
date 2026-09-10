import django_filters

from app.subscription.models import Subscription


class CharInFilter(
    django_filters.BaseInFilter,
    django_filters.CharFilter,
):
    pass


class SubscriptionFilter(django_filters.FilterSet):
    status__in = CharInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = Subscription
        fields = ["status"]  # noqa
