from fastapi import FastAPI, HTTPException, Body, Depends
from sql_app import models
from sql_app.database import engine, get_db
from sql_app import sql_main
import redis
from sqlalchemy.orm import Session
import json
from sql_app.schemas import JobBase,JobCreate,JobStatus, City, crawler_status, CrawlerStatus, UpdateJobStatusRequest
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


@app.get("/send_job", include_in_schema=False)
async def send_job(db: Session = Depends(get_db)):
    try:
        job_json = redis_client.rpop("jobs_queue")
        if not job_json:
            raise HTTPException(status_code=404, detail="No jobs in the queue")
        
        job_data = json.loads(job_json)
        job_id = job_data["id"]
        
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found in the database")

        job.status = JobStatus.in_progress
        db.commit()
        db.refresh(job)

        return job_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crawler-status/", include_in_schema=False)
def update_crawler_status(status: CrawlerStatus):
    crawler_status["status"] = status.status
    return {"message": "Status updated"}


@app.get("/crawler-status/")
def get_crawler_status():
    return crawler_status

@app.get("/status/{job_id}", response_model=JobStatus)
async def get_status(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.get_status()



@app.put("/update-job-status/{job_id}", response_model=JobBase)
async def update_job_status(job_id: int, request: UpdateJobStatusRequest, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job.status = request.status
    db.commit()
    db.refresh(job)
    
    return job