from typing import List

from sqlalchemy import (
    Column,
    Text,
    String,
    Boolean,
    DateTime,
    ARRAY,
    Integer,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.orm import Base


# youtube video data ------------------------------------------------------------------------------


# TODO: if relationships doesn't create those attributes in the table, create them manually (with additional attributes)
class YoutubeVideo(Base):
    __tablename__ = "youtube_video"

    title: Mapped[str] = mapped_column(String(100))  # youtube char limit for title
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(
        String(5000)
    )  # youtube char limit for description
    category: Mapped[str] = mapped_column(String, index=True)
    duration: Mapped[int] = mapped_column(Integer)  # video duration (in seconds)
    keywords: Mapped[List[str]] = mapped_column(ARRAY(String))
    uploaded_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    published_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    is_family_friendly: Mapped[bool] = mapped_column(Boolean)
    requires_subscription: Mapped[bool] = mapped_column(Boolean)

    creator: Mapped["Creator"] = relationship(back_populates="videos")

    thumbnails: Mapped[List["Media"]] = relationship(
        default=[], back_populates="thumbnail_for", cascade="all, delete-orphan"
    )
    video: Mapped["Media"] = relationship(
        back_populates="video_for", cascade="all, delete-orphan"
    )  # storage url of actual video


class Media(Base):
    __table__ = "media"

    url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)

    thumbnail_for: Mapped["YoutubeVideo"] = relationship(
        back_populates="thumbnails", single_parent=True
    )
    video_for: Mapped["YoutubeVideo"] = relationship(
        back_populates="video", single_parent=True
    )


class Creator(Base):
    __table__ = "creator"

    url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    videos: Mapped[List["YoutubeVideo"]] = relationship(
        back_populates="creator", cascade="all, delete-orphan"
    )


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
    title: Mapped[str] = mapped_column(String)
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
