from sqlalchemy import Integer, DateTime
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
