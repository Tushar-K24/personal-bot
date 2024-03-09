from typing import List

from sqlalchemy import Column, Text, String, DateTime, ARRAY, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.orm import Base


# User History (Youtube Watch History For Now) ------------------------------------------------------

user_details = Table(
    "user_details",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user_history.id")),
    Column("detail_id", Integer, ForeignKey("detail.id")),
)

user_subtitles = Table(
    "user_subtitles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user_history.id")),
    Column("subtitle_id", Integer, ForeignKey("subtitle.id")),
)


class UserHistory(Base):
    __tablename__ = "user_history"

    header: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(100))
    titleUrl: Mapped[str] = mapped_column(String)
    time: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    products: Mapped[List[str]] = mapped_column(ARRAY(String))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    activityControls: Mapped[List[str]] = mapped_column(ARRAY(String))
    htmlPage: Mapped[str] = mapped_column(Text, default="")

    details: Mapped[List["Detail"]] = relationship(
        secondary=user_details,
        back_populates="user_histories",
    )

    subtitles: Mapped[List["Subtitle"]] = relationship(
        secondary=user_subtitles,
        back_populates="user_histories",
    )

    # adding backref to UserDocumentChunks
    document_chunks: Mapped[List["UserDocumentChunk"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )


class Detail(Base):
    __tablename__ = "detail"

    name: Mapped[str] = mapped_column(String, index=True, unique=True)

    user_histories: Mapped[List["UserHistory"]] = relationship(
        secondary=user_details,
        back_populates="details",
    )


class Subtitle(Base):
    __tablename__ = "subtitle"

    name: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, index=True, unique=True)

    user_histories: Mapped[List["UserHistory"]] = relationship(
        secondary=user_subtitles,
        back_populates="subtitles",
    )


# ---------------------------------------------------------------------------------------------------


# Generic Document Chunks (for RAG)
class UserDocumentChunk(Base):
    __tablename__ = "user_document_chunk"

    text: Mapped[str] = mapped_column(Text)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_history.id"))

    parent: Mapped["UserHistory"] = relationship(back_populates="document_chunks")
