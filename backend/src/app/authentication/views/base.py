from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(
    summary="Health check",
    description="Verify that the API is running",
    tags=["System"],
)
class PingView(APIView):
    def get(self, request: Request) -> Response:  # noqa: ARG002
        return Response(
            {
                "status": "ok",
                "service": settings.APP_NAME,
                "version": settings.APP_VERSION,
            }
        )
