from sqlalchemy import Column, Integer, String
from .database import Base
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.sqlite import JSON


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    city_ids = Column(MutableList.as_mutable(JSON), default=[])
    category = Column(String, index=True, nullable=True)
    query = Column(String, index=True, nullable=True)
    num_posts = Column(Integer, default=10)