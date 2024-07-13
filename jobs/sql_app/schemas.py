from pydantic import BaseModel
from typing import List, Optional
from sql_app.models import JobStatus
class JobBase(BaseModel):
    city_ids: List[str]
    category: Optional[str] = None
    query: Optional[str] = None
    num_posts: int = 10

class JobCreate(BaseModel):
    city_names: List[str]
    category: Optional[str] = None
    query: Optional[str] = None
    num_posts: int = 10

class JobResponse(JobBase):
    id: int
    status: JobStatus = JobStatus.in_queue

    class Config:
        from_attributes = True

        

class PostBase(BaseModel):
    title: str
    token: str
    city: str
    district: str
    url: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

    class Config:
        from_attributes = True
