from fastapi import FastAPI
from sql_app import models
from sql_app.database import engine
from app import jobs, posts, status, crawler, queue


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(jobs.router, tags=["Jobs"])
app.include_router(posts.router, tags=["Posts"])
app.include_router(status.router, prefix="/status", tags=["Status"])
app.include_router(crawler.router, prefix="/crawler", tags=["Crawler"])
app.include_router(queue.router, prefix="/queue", tags=["Queue"])
