from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sql_app import models
from sql_app.database import engine, get_db
from sql_app import sql_main
from sqlalchemy.orm import Session
import requests
from datetime import datetime, timedelta
from sql_app.crud import create_post, delete_posts
from sql_app.schemas import PostCreate, Post, TaskResponse
from typing import List, Optional
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import threading

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)
active_tasks_lock = threading.Lock()
active_tasks = 0

app.include_router(sql_main.router, prefix="/api/v1")


class CityIDRequest(BaseModel):
    id: int
    city_ids: List[str]
    category: Optional[str] = None
    query: Optional[str] = None
    num_posts: Optional[int] = 10


is_busy = False


def update_job_status(job_id: int, status: str, message: Optional[str] = None):
    url = f"http://jobs_service:8000/status/update-job-status/{job_id}"
    data = {"status": status, "message": message}
    response = requests.put(url, json=data)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to update job status"
        )


def fetch_data_task(request: CityIDRequest, db: Session):
    global active_tasks
    with active_tasks_lock:
        active_tasks += 1

    fastapi_save_posts_url = "http://jobs_service:8000/save-posts/"
    job_id = request.id

    try:
        update_job_status(job_id, "in_progress")

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
                        url=f'https://divar.ir/v/{post_dict["action"]["payload"]["token"]}',
                    )
                    saved_post = create_post(db=db, post=post)
                    saved_posts.append(saved_post)
                    all_saved_posts.append(saved_post)

                    if len(all_saved_posts) >= posts_to_save:
                        break

            page += 1
            layer_page += 1

        post_data = [
            {
                "title": post.title,
                "token": post.token,
                "city": post.city,
                "district": post.district,
                "url": post.url,
            }
            for post in all_saved_posts
        ]

        response = requests.post(fastapi_save_posts_url, json=post_data)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to send data to job service",
            )

        delete_posts(db, all_saved_posts)
        update_job_status(job_id, "completed")

    except Exception as e:
        update_job_status(job_id, "failed", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        with active_tasks_lock:
            active_tasks -= 1


@app.post("/fetch-data", response_model=TaskResponse)
def fetch_data(
    request: CityIDRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    background_tasks.add_task(executor.submit, fetch_data_task, request, db)
    return {"message": "Task started"}


@app.get("/status", include_in_schema=False)
def get_status():
    global active_tasks
    with active_tasks_lock:
        return {"status": "busy" if active_tasks == 4 else "free"}
