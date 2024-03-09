from datetime import datetime
from typing import List, Optional

from app.models.pydantic.base import Base


class Detail(Base):
    name: str


class Subtitle(Base):
    name: str
    url: str


class UserHistory(Base):
    header: str
    title: str
    titleUrl: str
    time: datetime
    products: List[str]
    details: Optional[List[Detail]] = []
    description: Optional[str] = None
    activityControls: List[str]
    htmlPage: Optional[str] = None
    subtitles: Optional[List[Subtitle]] = []
