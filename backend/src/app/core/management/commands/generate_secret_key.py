from typing import Any

from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = "Generate a Django SECRET_KEY"

    def handle(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        secret = get_random_secret_key()
        # Escape '$' so Docker Compose does not try to expand it
        secret = secret.replace("$", "$$")

        self.stdout.write(f"New Django SECRET_KEY:\n{secret}")
