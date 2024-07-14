import requests
from celery import Celery

celery_app = Celery("worker")


@celery_app.task
def fetch_status_and_process_job():
    status_url = "http://crawler_service:8001/status"
    send_job_url = "http://jobs_service:8000/send_job"
    fetch_data_url = "http://crawler_service:8001/fetch-data"

    try:
        # Check the status
        status_response = requests.get(status_url)
        status_response.raise_for_status()
        status_data = status_response.json()

        if status_data.get("status") == "free":
            # Fetch the job
            job_response = requests.get(send_job_url)
            job_response.raise_for_status()
            job_data = job_response.json()

            # Send the job to fetch-data
            fetch_response = requests.post(fetch_data_url, json=job_data)
            fetch_response.raise_for_status()
            fetch_result = fetch_response.json()

            print(f"Fetched data: {fetch_result}")

    except requests.exceptions.RequestException as e:
        print(f"Error during fetch_status_and_process_job: {e}")