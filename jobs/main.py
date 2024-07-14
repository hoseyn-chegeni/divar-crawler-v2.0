from fastapi import FastAPI, HTTPException, Body, Depends
from sql_app import models
from sql_app.database import engine, get_db
from sql_app import sql_main
import requests
import redis
from sqlalchemy.orm import Session
import json
from sql_app.schemas import JobCreate, City
from sql_app import crud


models.Base.metadata.create_all(bind=engine)
redis_client = redis.Redis(host="redis", port=6379)

app = FastAPI()
app.include_router(sql_main.router, prefix="/api/v1")



@app.post("/save_job/")
async def send_job(job_request: JobCreate = Body(...), db: Session = Depends(get_db)):
    try:
        city_ids = [
            City[city.replace(" ", "_").upper()].value
            for city in job_request.city_names
        ]
    except KeyError as e:
        raise HTTPException(
            status_code=400, detail=f"City name {e.args[0]} is not recognized"
        )
    db_job = crud.create_job(db, job_request, city_ids)
    job_json = json.dumps(
        {
            "id": db_job.id,
            "city_ids": city_ids,
            "category": db_job.category,
            "query": db_job.query,
            "num_posts": db_job.num_posts,
            "status": db_job.status,
        }
    )
    redis_client.lpush("jobs_queue", job_json)
    return {"message": "Job sent to the queue", "data": job_json}


@app.get("/queue_instances")
async def get_queue_instances():
    queue_length = redis_client.llen("jobs_queue")
    instances = [
        json.loads(redis_client.lindex("jobs_queue", i)) for i in range(queue_length)
    ]
    return {"instances_in_queue": instances}


@app.get("/send_job")
async def send_job():
    try:
        job_json = redis_client.rpop("jobs_queue")
        if not job_json:
            raise HTTPException(status_code=404, detail="No jobs in the queue")
        job = json.loads(job_json)
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))