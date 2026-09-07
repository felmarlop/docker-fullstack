from django.urls import path

from app.subscription.views import subscription

urlpatterns = [
    path("subscription/create/", subscription.SubscriptionView.as_view(), name="create-subscription"),
]
