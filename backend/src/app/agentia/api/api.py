import logging
from datetime import datetime

from django.conf import settings
from google import genai
from google.genai import errors, types

from app.agentia.api.exceptions import (
    AgentClientError,
    AgentGeneralError,
    AgentServerError,
)

logger = logging.getLogger(__name__)
current_date = datetime.now().strftime("%A, %B %d, %Y")

GEMINI_MODEL = "gemini-3.1-flash-lite"
SYS_INSTRUCTION = (
    f"Your name is {settings.AI_AGENT_NAME}, an AI assitant. "
    f"Today's date is {current_date}. "
    f"OUTPUT FORMAT: Keep all responses under 2-3 sentences. Return direct answers."
)


class GeminiAPI:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

        config = types.GenerateContentConfig(
            system_instruction=SYS_INSTRUCTION,
            temperature=0.3,  # temperature for API routing, function calling, math...
        )
        self.chat = self.client.chats.create(model=GEMINI_MODEL, config=config)
        logger.info(f"{settings.AI_AGENT_NAME} has been initialized successfully.")

    def __str__(self) -> str:
        return f"GeminiAPI(model={GEMINI_MODEL})"

    def send_message(self, prompt: str) -> str:
        try:
            response = self.chat.send_message(prompt)
        except errors.ClientError as exc:
            raise AgentClientError from exc
        except errors.ServerError as exc:
            raise AgentServerError from exc
        except errors.APIError as exc:
            raise AgentGeneralError from exc

        return response.text or ""
