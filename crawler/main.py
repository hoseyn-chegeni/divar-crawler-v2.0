from fastapi import FastAPI
from sql_app import models
from sql_app.database import engine
from sql_app import sql_main

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(sql_main.router, prefix="/api/v1")


