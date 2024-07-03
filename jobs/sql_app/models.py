from sqlalchemy import Column,Integer, String
from .database import Base


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

