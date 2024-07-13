from sqlalchemy import Column, Integer, String, Enum
from .database import Base
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.sqlite import JSON
import enum


class JobStatus(str, enum.Enum):
    in_queue = "in queue"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    city_ids = Column(MutableList.as_mutable(JSON), default=[])
    category = Column(String, index=True, nullable=True)
    query = Column(String, index=True, nullable=True)
    num_posts = Column(Integer, default=10)
    status = Column(Enum(JobStatus), default=JobStatus.in_queue, nullable=False)

    def get_status(self):
        return self.status


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    token = Column(String, unique=True, index=True)
    city = Column(String, index=True)
    district = Column(String, index=True)
    url = Column(String, index=True)
