from celery import Celery

celery_app = Celery(
    "worker", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)

celery_app.conf.beat_schedule = {
    "check-crawler-status-every-10-seconds": {
        "task": "tasks.fetch_status",
        "schedule": 10.0,
    },
}

celery_app.conf.timezone = "UTC"


import tasks