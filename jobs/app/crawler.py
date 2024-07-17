from fastapi import APIRouter
from sql_app.schemas import crawler_status, CrawlerStatus

router = APIRouter()


@router.post("/status/", include_in_schema=False)
def update_crawler_status(status: CrawlerStatus):
    crawler_status["status"] = status.status
    return {"message": "Status updated"}


@router.get("/status/")
def get_crawler_status():
    return crawler_status
