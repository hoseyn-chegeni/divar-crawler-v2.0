from fastapi import FastAPI, HTTPException, Body, Depends
from sql_app import models
from sql_app.database import engine, get_db
from sql_app import sql_main
import requests
import redis
from sqlalchemy.orm import Session
import json
from sql_app.schemas import JobCreate
from sql_app import crud

models.Base.metadata.create_all(bind=engine)
redis_client = redis.Redis(host="redis", port=6379)

app = FastAPI()
app.include_router(sql_main.router, prefix="/api/v1")


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
async def send_job(job_request: JobCreate = Body(...), db: Session = Depends(get_db)):
    # Create job in the database
    db_job = crud.create_job(db, job_request)

    # Convert the Job instance to JSON
    job_json = json.dumps(
        {
            "id": db_job.id,
            "city_ids": db_job.city_ids,
            "category": db_job.category,
            "query": db_job.query,
            "num_posts": db_job.num_posts,
            "status": db_job.status,

        }
    )

    # Push job to Redis queue
    redis_client.lpush("jobs_queue", job_json)

    return {"message": "Job sent to the queue", "data": job_json}


@app.get("/queue_instances")
async def get_queue_instances():
    # Retrieve all elements in the queue
    queue_length = redis_client.llen("jobs_queue")
    instances = [
        json.loads(redis_client.lindex("jobs_queue", i)) for i in range(queue_length)
    ]

    return {"instances_in_queue": instances}

@app.get("/job_status/{job_id}", response_model=str)
async def get_job_status(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job.get_status()
