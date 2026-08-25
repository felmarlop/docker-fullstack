from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.authentication.serializers.social import GithubSerializer, GoogleSerializer


class GoogleView(APIView):
    """
    Authenticate a user with Google.
    """

    serializer_class = GoogleSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data)


class GithubView(APIView):
    """
    Authenticate a user with GitHub.
    """

    serializer_class = GithubSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data)
