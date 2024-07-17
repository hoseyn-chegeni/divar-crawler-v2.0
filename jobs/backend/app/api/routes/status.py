from fastapi import HTTPException, Depends, APIRouter
from backend.app import models
from backend.app.core.db import get_db
from sqlalchemy.orm import Session
from backend.app.schemas import (
    JobBase,
    JobStatus,
    crawler_status,
    UpdateJobStatusRequest,
)


router = APIRouter()


@router.get("/{job_id}", response_model=JobStatus)
async def get_status(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.get_status()


@router.put(
    "/update-job-status/{job_id}", response_model=JobBase, include_in_schema=False
)
async def update_job_status(
    job_id: int, request: UpdateJobStatusRequest, db: Session = Depends(get_db)
):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.status = request.status
    db.commit()
    db.refresh(job)

    return job
