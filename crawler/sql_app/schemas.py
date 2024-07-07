from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    token: str
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

    class Config:
        orm_mode = True