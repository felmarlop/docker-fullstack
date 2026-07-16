from django.urls import path

from app.authentication.views import PingView

urlpatterns = [
    path("ping/", PingView.as_view(), name="ping"),
]
