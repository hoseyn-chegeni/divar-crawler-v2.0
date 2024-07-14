import requests
from celery import Celery

celery_app = Celery("worker")

@celery_app.task
def fetch_status():
    url = "http://crawler_service:8001/status"  # Update if the server URL is different
    try:
        response = requests.get(url)
        response.raise_for_status()
        status_data = response.json()
        print(f"Status: {status_data}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching status: {e}")
