from rest_framework.exceptions import APIException


class GeminiGeneralError(APIException):
    status_code = 502
    default_detail = "An error occurred while communicating with Gemini."
    default_code = "gemini_general_error"


class GeminiClientError(APIException):
    status_code = 502
    default_detail = "Gemini rejected the request."
    default_code = "gemini_client_error"


class GeminiServerError(APIException):
    status_code = 503
    default_detail = "Gemini service is temporarily unavailable."
    default_code = "gemini_server_error"
