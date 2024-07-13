from sqlalchemy.orm import Session
from sql_app.models import Job, Post
from sql_app.schemas import JobCreate, JobStatus, PostCreate
from typing import List


def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Job).offset(skip).limit(limit).all()


def create_job(db: Session, job_request: JobCreate, city_ids: List[int]):
    db_job = Job(
        city_ids=city_ids,
        category=job_request.category,
        query=job_request.query,
        num_posts=job_request.num_posts,
        status=JobStatus.in_queue,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job_status(db: Session, job_id: int, status: JobStatus):
    job = get_job(db, job_id)
    if job:
        job.status = status
        db.commit()
        db.refresh(job)
    return job


def create_post(db: Session, post: PostCreate):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()
