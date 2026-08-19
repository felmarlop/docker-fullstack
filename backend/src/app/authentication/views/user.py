from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.authentication.serializers.account import UpdateProfileSerializer
from app.authentication.serializers.user import UserSerializer


@extend_schema(
    summary="Current user",
    description="Return the authenticated user's information",
    tags=["Users"],
    responses={200: UserSerializer},
)
@extend_schema(
    methods=["PUT"],
    summary="Update current user",
    description="Update the authenticated user's personal information",
    request=UpdateProfileSerializer,
    tags=["Users"],
    responses={200: UserSerializer},
)
class MeView(APIView):
    permission_classes = [IsAuthenticated]  # noqa

    def get(self, request: Request) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request: Request) -> Response:
        serializer = UpdateProfileSerializer(
            instance=request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response(UserSerializer(user).data)
