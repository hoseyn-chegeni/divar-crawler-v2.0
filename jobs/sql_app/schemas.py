from pydantic import BaseModel
from typing import List



class JobBase(BaseModel):
    title: str
    description: str


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int

    class Config:
        orm_mode = True
