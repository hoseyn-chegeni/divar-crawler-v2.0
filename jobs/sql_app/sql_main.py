from celery import Celery
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import get_db
from typing import List
import redis


celery = Celery(
    __name__,
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


router = APIRouter()


@celery.task
def add_job_to_queue(job_id: int):
    # Simulate adding the job to the queue
    return {"status": f"Job {job_id} added to queue"}

@router.post("/jobs/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    job = crud.create_job(db=db, job=job)
    add_job_to_queue.delay(job.id)
    return job

@router.get("/jobs/", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs

@router.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job
