# Use an official Python runtime as a parent image
FROM python:3.11.4-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

COPY requirements.txt /app/requirements.txt

# Install any dependencies
RUN pip install -r /app/requirements.txt

# Expose port 8000 for the jobs service
EXPOSE 8000

# Command to run the jobs service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
