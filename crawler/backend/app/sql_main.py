from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .crud import get_posts, create_post, delete_posts
from .schemas import Post
from backend.app.core.db import get_db
from typing import List


# Initialize the FastAPI router
router = APIRouter()


@router.get("/posts/", response_model=List[Post], include_in_schema=False)
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = get_posts(db, skip=skip, limit=limit)
    return posts
