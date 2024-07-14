from celery import Celery
import tasks

celery_app = Celery(
    "worker", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)
celery_app.conf.timezone = "UTC"


