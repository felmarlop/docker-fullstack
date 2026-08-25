from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.authentication"

    def ready(self) -> None:
        import app.authentication.signals  # noqa: F401
