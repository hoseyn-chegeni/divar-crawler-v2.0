from pydantic import BaseModel


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
        orm_mode = True


class TaskResponse(BaseModel):
    message: str
