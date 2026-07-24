from typing import Any

from django.core.management.base import BaseCommand

from app.core.periodic_tasks import setup_periodic_tasks


class Command(BaseCommand):
    help = "Create or update the default periodic Celery tasks."

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ARG002
        setup_periodic_tasks()
        self.stdout.write(self.style.SUCCESS("Periodic tasks configured successfully."))
