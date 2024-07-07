
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
import requests

from .crud import get_posts, create_post
from .schemas import Post, PostCreate
from.models import Base
from .database import SessionLocal, engine, get_db
from typing import List
from pydantic import BaseModel




router = APIRouter()



class CityIDRequest(BaseModel):
    city_ids: List[str]

@router.post("/fetch-data", response_model=List[Post])
def fetch_data(request: CityIDRequest, db: Session = Depends(get_db)):
    url = "https://api.divar.ir/v8/postlist/w/search"
    headers = {"Content-Type": "application/json"}
    
    # Define the body with the predefined structure and add the city_id
    body = {
        "city_ids": request.city_ids,
        "search_data": {
            "form_data": {
                "data": {
                    "category": {
                        "str": {
                            "value": "ROOT"
                        }
                    }
                }
            }
        }
    }
    
    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")

    data = response.json()
    
    # Extract list_widgets
    post_data = data.get('list_widgets', [])
    
    # Filter and save posts to the database
    saved_posts = []
    for item in post_data:
        if item.get('data', {}).get('@type') == 'type.googleapis.com/widgets.PostRowData':
            post_dict = item['data']
            post = PostCreate(
                title=post_dict['title'],
                token=post_dict['action']['payload']['token']
            )
            saved_post = create_post(db=db, post=post)
            saved_posts.append(saved_post)
    
    return saved_posts

@router.get("/posts/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = get_posts(db, skip=skip, limit=limit)
    return posts
