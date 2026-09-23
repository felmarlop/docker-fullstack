from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.authentication import utils
from app.authentication.models import User
from app.authentication.serializers.account import UpdateProfileSerializer
from app.authentication.serializers.user import UserSerializer
from app.authentication.views.filters import UserFilter
from app.core.pagination import DefaultPagination


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
    responses={200: UserSerializer},
    tags=["Users"],
)
class MeView(APIView):
    permission_classes = [IsAuthenticated]  # noqa

    def get(self, request: Request) -> Response:
        return Response(utils.serialize_user(request.user, request))

    def put(self, request: Request) -> Response:
        serializer = UpdateProfileSerializer(
            instance=request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response(utils.serialize_user(user, request))  # type: ignore


@extend_schema(
    summary="List users",
    description="Return all the users in the system.",
    tags=["Users"],
    responses={200: UserSerializer(many=True)},
)
class UserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # noqa
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # noqa
    ordering_fields = ["date_joined", "username", "email"]  # noqa
    ordering = ["-date_joined"]  # noqa
    pagination_class = DefaultPagination

    def get_queryset(self) -> QuerySet[User]:  # pyright: ignore[reportIncompatibleMethodOverride]
        return User.objects.all().order_by("-date_joined")
