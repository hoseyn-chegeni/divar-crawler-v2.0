from fastapi import FastAPI, HTTPException
from sql_app import models
from sql_app.database import engine
from sql_app import sql_main
import requests

models.Base.metadata.create_all(bind=engine)

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
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch crawler status")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Crawler service is not available") from e