from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import requests
from datetime import datetime, timedelta
from .crud import get_posts, create_post, delete_posts
from .schemas import Post, PostCreate
from .database import get_db
from typing import List, Optional
from pydantic import BaseModel


# Initialize the FastAPI router
router = APIRouter()


@router.get("/posts/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = get_posts(db, skip=skip, limit=limit)
    return posts
