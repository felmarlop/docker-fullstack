from django_celery_beat.models import IntervalSchedule, PeriodicTask


def create_heartbeat_task() -> None:
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.update_or_create(
        name="Heartbeat",
        defaults={
            "task": "app.authentication.tasks.heartbeat",
            "interval": interval,
            "enabled": True,
        },
    )


def setup_periodic_tasks() -> None:
    """
    Create or update the default periodic tasks for the project.
    """
    create_heartbeat_task()
