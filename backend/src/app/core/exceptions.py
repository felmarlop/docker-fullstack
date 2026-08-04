from typing import Any

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(
    exc: APIException, context: dict[str, Any]
) -> Response | None:
    response = exception_handler(exc, context)

    if response is None:
        return None

    if hasattr(exc, "get_codes"):
        response.data["code"] = exc.get_codes()  # type: ignore

    return response
