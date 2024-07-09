from celery import shared_task
import requests


@shared_task
def check_crawler_status_task():
    try:
        # Replace with the actual URL of your FastAPI server
        fastapi_url = "http://jobs_service:8000/crawler-status"

        response = requests.get(fastapi_url)

        if response.status_code == 200:
            status = response.json()
            print(f"Crawler status: {status['crawler_status']}")
        else:
            print(f"Failed to fetch crawler status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling check_crawler_status: {str(e)}")
