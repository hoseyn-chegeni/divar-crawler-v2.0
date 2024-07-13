from sqlalchemy.orm import Session
from typing import List
from . import schemas
from . import models


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()


def delete_posts(db: Session, posts: List[models.Post]):
    post_ids = [post.id for post in posts]
    db.query(models.Post).filter(models.Post.id.in_(post_ids)).delete(synchronize_session='fetch')
    db.commit()