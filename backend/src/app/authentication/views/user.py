from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.authentication.serializers.user import UserSerializer


class MeView(APIView):
    """
    Return the authenticated user.
    """

    permission_classes = [IsAuthenticated]  # noqa

    def get(self, request: Request) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
