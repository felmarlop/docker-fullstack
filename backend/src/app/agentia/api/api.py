from django.conf import settings
from google import genai
from google.genai import errors

from app.agentia.api.exceptions import (
    GeminiClientError,
    GeminiGeneralError,
    GeminiServerError,
)

GEMINI_MODEL = "gemini-3.1-flash-lite"


class GeminiAPI:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def __str__(self) -> str:
        return f"GeminiAPI(model={GEMINI_MODEL})"

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
        except errors.ClientError as exc:
            raise GeminiClientError from exc
        except errors.ServerError as exc:
            raise GeminiServerError from exc
        except errors.APIError as exc:
            raise GeminiGeneralError from exc

        return response.text or ""
