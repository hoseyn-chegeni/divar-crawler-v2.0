# Use the official Python image from the Docker Hub
FROM python:3.11.4-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install any dependencies
RUN pip install  -r /app/requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . /app

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Run the application
CMD ["sh", "-c", "uvicorn backend.app.api.main:app --host 0.0.0.0 --port 8001 --reload & sleep 10 && celery -A backend.app.CELERY beat --loglevel=info"]
