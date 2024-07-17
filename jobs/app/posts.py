from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sql_app import crud
from sql_app.database import get_db
from typing import List, Optional
from sql_app.schemas import PostCreate, Post


router = APIRouter()


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
def read_posts(
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    city: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db),
):
    posts = crud.get_posts(
        db, skip=skip, limit=limit, title=title, city=city, district=district
    )
    return posts
