from django.urls import path

from app.agentia.views import AgentIaView

urlpatterns = [path("ai/agent/", AgentIaView.as_view(), name="ai-agent")]
