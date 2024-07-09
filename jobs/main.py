from fastapi import FastAPI, HTTPException, Body
from sql_app import models
from sql_app.database import engine
from sql_app import sql_main
import requests
from pydantic import BaseModel
from celery import shared_task
import redis


models.Base.metadata.create_all(bind=engine)
redis_client = redis.Redis(host='redis', port=6379)

app = FastAPI()
app.include_router(sql_main.router, prefix="/api/v1")


class CityIDRequest(BaseModel):
    city_ids: list[str]
    category: str = None
    query: str = None
    num_posts: int = 10


@app.get("/crawler-status")
def check_crawler_status():
    crawler_url = "http://crawler_service:8001/api/v1/status"
    try:
        response = requests.get(crawler_url)
        if response.status_code == 200:
            status = response.json()
            return {"crawler_status": status["status"]}
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch crawler status",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail="Crawler service is not available"
        ) from e



@app.post("/send_job/")
async def send_job(request: CityIDRequest = Body(...)):
    # Push job to Redis queue
    redis_client.lpush('jobs_queue', request.json())
    return {"message": "Job sent to the queue", "data": request.dict()}

@app.get("/queue_instances")
async def get_queue_instances():
    # Retrieve all elements in the queue
    queue_length = redis_client.llen('jobs_queue')
    instances = [redis_client.lindex('jobs_queue', i) for i in range(queue_length)]
    return {"instances_in_queue": instances}