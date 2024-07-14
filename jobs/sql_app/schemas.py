from pydantic import BaseModel
from typing import List, Optional
from sql_app.models import JobStatus
from enum import Enum


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


class City(Enum):
    TEHRAN = "1"
    KARAJ = "2"
    MASHHAD = "3"
    ISFAHAN = "4"
    TABRIZ = "5"
    SHIRAZ = "6"
    AHWAZ = "7"
    QOM = "8"
    KERMANSHAH = "9"
    URMIA = "10"
    ZAHEDAN = "11"
    RASHT = "12"
    KERMAN = "13"
    HAMADAN = "14"
    ARAK = "15"
    YAZD = "16"
    ARDABIL = "17"
    BANDAR_ABBAS = "18"
    QAZVIN = "19"
    ZANJAN = "20"
    GORGAN = "21"
    SARI = "22"
    DEZFUL = "23"
    ABADAN = "24"
    BUSHEHR = "25"
    BORUJERD = "26"
    KHORAM_ABAD = "27"
    SANANDAJ = "28"
    ESLAMSHAHR = "29"
    KASHAN = "30"
    NAJAFABAD = "31"
    ILAM = "32"
    KISH = "33"
    BIRJAND = "34"
    SEMNAN = "35"
    SHAHREKORD = "36"
    BANDAR_MAHSHAR = "37"
    YASUJ = "38"
    BOJNURD = "39"
