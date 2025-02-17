from sqlalchemy import Column, Integer, String, Boolean
from backend.app.core.db import get_db, Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    token = Column(String, unique=True, index=True)
    city = Column(String, index=True)
    district = Column(String, index=True)
    url = Column(String, index=True)
