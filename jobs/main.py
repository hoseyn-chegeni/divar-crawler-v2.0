from fastapi import FastAPI, HTTPException, Body, Depends
from sql_app import models
from sql_app.database import engine, get_db
from sql_app import sql_main
import requests
import redis
from sqlalchemy.orm import Session
import json
from sql_app.schemas import JobCreate, City
from sql_app import crud
from pydantic import BaseModel


models.Base.metadata.create_all(bind=engine)
redis_client = redis.Redis(host="redis", port=6379)

app = FastAPI()
app.include_router(sql_main.router, prefix="/api/v1")

