from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import requests
from datetime import datetime, timedelta
from .crud import get_posts, create_post
from .schemas import Post, PostCreate
from .database import get_db
from typing import List, Optional
from pydantic import BaseModel


# Initialize the FastAPI router
router = APIRouter()


class CityIDRequest(BaseModel):
    id: int
    city_ids: List[str]
    category: Optional[str] = None
    query: Optional[str] = None
    num_posts: Optional[int] = 10


is_busy = False

@router.post("/fetch-data", response_model=List[Post])
def fetch_data(request: CityIDRequest, db: Session = Depends(get_db)):
    fastapi_update_status_url = "http://jobs_service:8000/update_job_status/"
    fastapi_save_posts_url = "http://jobs_service:8000/api/v1/save-posts/"
    global is_busy
    is_busy = True
    try:
        url = "https://api.divar.ir/v8/postlist/w/search"
        headers = {"Content-Type": "application/json"}

        page = 1
        layer_page = 1
        last_post_date = datetime.utcnow()

        all_saved_posts = []
        posts_to_save = request.num_posts

        while page <= 10 and len(all_saved_posts) < posts_to_save:
            last_post_date -= timedelta(minutes=30)
            body = {
                "city_ids": request.city_ids,
                "search_data": {"form_data": {"data": {}}},
                "pagination_data": {
                    "@type": "type.googleapis.com/post_list.PaginationData",
                    "last_post_date": last_post_date.isoformat() + "Z",
                    "layer_page": layer_page,
                    "page": page,
                    "search_uid": "d33a69a6-d2cc-4b10-8ae4-2d47c4e3a8bf",
                },
            }

            if request.category:
                body["search_data"]["form_data"]["data"]["category"] = {
                    "str": {"value": request.category}
                }
            else:
                body["search_data"]["form_data"]["data"]["category"] = {
                    "str": {"value": "ROOT"}
                }

            if request.query:
                body["search_data"]["query"] = request.query

            response = requests.post(url, json=body, headers=headers)

            if response.status_code != 200:
                requests.put(
                fastapi_update_status_url,
                json={"job_id": request.id, "status": "failed"}
                )
                raise HTTPException(
                    status_code=response.status_code, detail="Failed to fetch data"
                )

            data = response.json()
            post_data = data.get("list_widgets", [])

            if not post_data:
                break

            saved_posts = []
            for item in post_data:
                if (
                    item.get("data", {}).get("@type")
                    == "type.googleapis.com/widgets.PostRowData"
                ):
                    post_dict = item["data"]
                    post = PostCreate(
                        title=post_dict["title"],
                        token=post_dict["action"]["payload"]["token"],
                        city=post_dict["action"]["payload"]["web_info"]["city_persian"],
                        district=post_dict["action"]["payload"]["web_info"][
                            "district_persian"
                        ],
                        url=f'https://divar.ir/v/{post_dict["action"]["payload"]["token"]}'
                    )
                    saved_post = create_post(db=db, post=post)
                    saved_posts.append(saved_post)
                    all_saved_posts.append(saved_post)

                    if len(all_saved_posts) >= posts_to_save:
                        break

            page += 1
            layer_page += 1

        # Send the data to job_service
        post_data = [
            {
                "title": post.title,
                "token": post.token,
                "city": post.city,
                "district": post.district,
                "url": post.url
            }
            for post in all_saved_posts
        ]

        response = requests.post(fastapi_save_posts_url, json=post_data)
        if response.status_code != 200:
            requests.put(
                fastapi_update_status_url,
                json={"job_id": request.id, "status": "failed"}
            )
            raise HTTPException(
                status_code=response.status_code, detail="Failed to send data to job service"
            )

    finally:
        is_busy = False

    return all_saved_posts



@router.get("/status")
def get_status():
    return {"status": "busy" if is_busy else "free"}


@router.get("/posts/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = get_posts(db, skip=skip, limit=limit)
    return posts
