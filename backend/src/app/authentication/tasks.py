from celery import shared_task


@shared_task
def hello() -> str:
    print("Hello from Celery!")

    return "Hello from Celery!"
