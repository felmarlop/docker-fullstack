from django.urls import path

from app.subscription.views import subscription

urlpatterns = [
    path(
        "subscription-plans/",
        subscription.SubscriptionPlansView.as_view(),
        name="subscription-plans",
    ),
    path(
        "subscriptions/<int:pk>/",
        subscription.SubscriptionDetailView.as_view(),
        name="subscription-detail",
    ),
    path(
        "subscriptions/",
        subscription.SubscriptionListView.as_view(),
        name="subscription-list",
    ),
    path(
        "subscriptions/create/",
        subscription.CreateSubscriptionView.as_view(),
        name="create-subscription",
    ),
    path(
        "subscriptions/<int:pk>/cancel/",
        subscription.CancelSubscriptionView.as_view(),
        name="cancel-subscription",
    ),
]
