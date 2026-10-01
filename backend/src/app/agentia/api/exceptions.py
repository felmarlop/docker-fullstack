from rest_framework.exceptions import APIException


class AgentGeneralError(APIException):
    status_code = 502
    default_detail = "An error occurred while communicating with the AI agent."
    default_code = "agent_general_error"


class AgentClientError(APIException):
    status_code = 502
    default_detail = "The AI agent rejected the request."
    default_code = "agent_client_error"


class AgentServerError(APIException):
    status_code = 503
    default_detail = "The AI agent is temporarily unavailable."
    default_code = "agent_server_error"
