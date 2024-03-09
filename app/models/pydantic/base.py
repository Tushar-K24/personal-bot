from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Base(BaseModel):
    id: Optional[int] = None
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None

    class Config:
        orm_mode = True
