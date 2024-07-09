from celery import shared_task
import requests
import json
from main import redis_client


@shared_task
def check_crawler_status_task():
    try:
        fastapi_status_url = "http://jobs_service:8000/crawler-status"
        fastapi_fetch_data_url = "http://crawler_service:8001/api/v1/fetch-data"

        response = requests.get(fastapi_status_url)

        if response.status_code == 200:
            status = response.json()
            if status['crawler_status'] == 'free':
                job_data = redis_client.rpop('jobs_queue')
                if job_data:
                    job_request = json.loads(job_data)
                    response = requests.post(fastapi_fetch_data_url, json=job_request)
                    if response.status_code == 200:
                        print("Job processed successfully")
                    else:
                        print(f"Failed to process job: {response.status_code}")
                else:
                    print("No jobs in the queue")
            else:
                print("Crawler is busy, skipping...")
        else:
            print(f"Failed to fetch crawler status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling check_crawler_status: {str(e)}")