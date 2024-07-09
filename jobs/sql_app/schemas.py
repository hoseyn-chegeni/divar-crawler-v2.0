from pydantic import BaseModel
from typing import List, Optional

class JobBase(BaseModel):
    city_ids: List[str]
    category: Optional[str] = None
    query: Optional[str] = None
    num_posts: int = 10

class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: int

    class Config:
        orm_mode = True
