
from fastapi import FastAPI
from sql_app import models
from sql_app.database import engine
from sql_app import main

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(main.router, prefix="/api/v1")