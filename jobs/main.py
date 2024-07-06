from fastapi import FastAPI
from sql_app import models
from sql_app.database import engine
from sql_app import main
from celery import Celery

models.Base.metadata.create_all(bind=engine)

celery = Celery(
    __name__,
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

app = FastAPI()

app.include_router(main.router, prefix="/api/v1")


@app.post("/task")
def run_task():
    task = example_task.delay()
    return {"task_id": task.id}

@celery.task
def example_task():
    return {"status": "Task completed"}