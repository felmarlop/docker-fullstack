from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.authentication.serializers.user import UserSerializer


@extend_schema(
    summary="Current user",
    description="Return the authenticated user's information",
    tags=["Users"],
    responses={200: UserSerializer},
)
class MeView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def get(self, request: Request) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
