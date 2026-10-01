import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_prompt_success(authenticated_api_client: APIClient) -> None:
    prompt = "hello! reply only with `Hello from Gemini!`"
    response = authenticated_api_client.post(
        reverse("ai-agent"),
        {
            "prompt": prompt,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    assert "prompt" in response.data
    assert "answer" in response.data

    assert response.data["prompt"]["content"] == prompt
    assert response.data["answer"]["content"] == "Hello from Gemini!"


@pytest.mark.django_db
def test_prompt_unauthorized(public_api_client: APIClient) -> None:
    response = public_api_client.post(
        reverse("ai-agent"),
        {
            "prompt": "hello!",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data
