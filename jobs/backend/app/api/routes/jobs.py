from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from backend.app import crud
from backend.app.core.db import get_db
from typing import List
from backend.app.schemas import JobCreate, JobResponse, City, JobStatus
import json
from backend.app.api.routes.queue import redis_client
from backend.app import models

router = APIRouter()


@router.post("/jobs/", response_model=JobResponse, include_in_schema=False)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db, job)


@router.get("/jobs/", response_model=List[JobResponse])
def read_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_jobs(db, skip=skip, limit=limit)


@router.post("/save_job/")
async def send_job(job_request: JobCreate = Body(...), db: Session = Depends(get_db)):
    try:
        city_ids = [
            City[city.replace(" ", "_").upper()].value
            for city in job_request.city_names
        ]
    except KeyError as e:
        raise HTTPException(
            status_code=400, detail=f"City name {e.args[0]} is not recognized"
        )
    db_job = crud.create_job(db, job_request, city_ids)
    job_json = json.dumps(
        {
            "id": db_job.id,
            "city_ids": city_ids,
            "category": db_job.category,
            "query": db_job.query,
            "num_posts": db_job.num_posts,
            "status": db_job.status,
        }
    )
    redis_client.lpush("jobs_queue", job_json)
    return {"message": "Job sent to the queue", "data": job_json}


@router.get("/send_job", include_in_schema=False)
async def send_job(db: Session = Depends(get_db)):
    try:
        job_json = redis_client.rpop("jobs_queue")
        if not job_json:
            raise HTTPException(status_code=404, detail="No jobs in the queue")

        job_data = json.loads(job_json)
        job_id = job_data["id"]

        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found in the database")

        job.status = JobStatus.in_progress
        db.commit()
        db.refresh(job)

        return job_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
