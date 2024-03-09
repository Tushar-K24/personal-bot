from app.base.base_repository import BaseRepository
from .model import Detail, Subtitle, UserHistory


class DetailRepository(BaseRepository):
    def getEntity(self) -> Detail:
        return Detail


class SubtitleRepository(BaseRepository):
    def getEntity(self) -> Subtitle:
        return Subtitle


class UserHistoryRepository(BaseRepository):
    def getEntity(self) -> UserHistory:
        return UserHistory
