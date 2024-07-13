from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud
from .database import get_db
from typing import List
from sql_app.schemas import JobCreate, JobResponse, PostCreate, Post



router = APIRouter()


@router.post("/jobs/", response_model=JobResponse, include_in_schema=False)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db, job)


@router.get("/jobs/", response_model=List[JobResponse])
def read_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_jobs(db, skip=skip, limit=limit)


@router.post("/save-posts/", response_model=List[Post], include_in_schema=False)
def save_posts(posts: List[PostCreate], db: Session = Depends(get_db)):
    saved_posts = []
    for post_data in posts:
        post = PostCreate(
            title=post_data.title,
            token=post_data.token,
            city=post_data.city,
            district=post_data.district,
            url=post_data.url,
        )
        saved_post = crud.create_post(db=db, post=post)
        saved_posts.append(saved_post)
    return saved_posts

@router.get("/posts/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts