FROM python:3.11.4-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONNUNBUFFERED = 1

COPY . /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload "]
