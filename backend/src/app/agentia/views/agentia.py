from typing import Any

from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.agentia.serializers import (
    AgentIaAnswerSerializer,
    AgentIaRequestSerializer,
)


@extend_schema(
    summary="AgentIA request",
    description="Send a prompt to AgentIA.",
    tags=["AgentIA"],
    request=AgentIaRequestSerializer,
    responses={200: AgentIaAnswerSerializer},
    examples=[
        OpenApiExample(
            "AgentIA request",
            value={
                "prompt": "Subscriptions purchased last month?",
            },
            request_only=True,
        ),
    ],
)
class AgentIaView(APIView):
    serializer_class = AgentIaRequestSerializer
    permission_classes = [IsAuthenticated]  # noqa

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        answer_msg, prompt_msg = serializer.generate()  # type: ignore
        response_serializer = AgentIaAnswerSerializer(
            {
                "prompt": prompt_msg,
                "answer": answer_msg,
            }
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)
