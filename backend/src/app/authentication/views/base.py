from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class PingView(APIView):
    """
    Simple endpoint used to verify that the API is running.
    """

    def get(self, request: Request) -> Response:  # noqa: ARG002
        return Response(
            {
                "status": "ok",
                "service": settings.APP_NAME,
                "version": settings.APP_VERSION,
            }
        )
