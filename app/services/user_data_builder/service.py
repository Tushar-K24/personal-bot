import json
import asyncio

from typing import Coroutine
from tqdm import tqdm

from app.settings.globals import SEARCH_HISTORY_PATH, DEFAULT_TITLE_URL
from app.utils.http_client import HTTPClient
from app.core.logger import logger
from app.utils.db_connection import init_db

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import DetailRepository, SubtitleRepository, UserHistoryRepository
from .schema import UserHistory, Detail, Subtitle
from .model import Detail as DetailModel
from .model import Subtitle as SubtitleModel
from .model import UserHistory as UserHistoryModel

lock = asyncio.Lock()
details: dict[str, DetailModel] = dict()


class UserDataBuilderService:
    # TODO: add support for multiple writes
    def __init__(self):
        self.details_repo = DetailRepository()
        self.subtitle_repo = SubtitleRepository()
        self.user_history_repo = UserHistoryRepository()

    async def get_details_or_create(
        self, detail: Detail, session: AsyncSession
    ) -> Coroutine[None, None, DetailModel]:
        detail = Detail(**detail).model_dump()
        name = detail["name"]
        if name in details:
            return details[name]
        await lock.acquire()
        try:
            _detail = await self.details_repo.create([detail], session=session)
            details[name] = _detail
            return _detail[0]
        finally:
            lock.release()

    async def get_subtitles_or_create(
        self, subtitle: Subtitle, session: AsyncSession
    ) -> Coroutine[None, None, SubtitleModel]:
        subtitle = Subtitle(**subtitle).model_dump()
        url = subtitle["url"]
        _subtitle = await self.subtitle_repo.find({"url": url}, session=session)
        if len(_subtitle) == 0:
            _subtitle = await self.subtitle_repo.create(subtitle, session=session)
        return _subtitle[0]

    async def _gather_data_and_ingest(
        self, client: HTTPClient, data: dict, session: AsyncSession
    ) -> None:
        try:
            if "titleUrl" not in data:
                data["titleUrl"] = DEFAULT_TITLE_URL
            res = await client.make_request(
                "GET",
                data["titleUrl"],
            )
            data["htmlPage"] = res["data"]
            data = UserHistory(**data).model_dump()
            data["details"] = [
                await self.get_details_or_create(detail, session)
                for detail in data["details"]
            ]
            data["subtitles"] = [
                await self.get_subtitles_or_create(subtitle, session)
                for subtitle in data["subtitles"]
            ]
            # details_coroutines = [
            #     asyncio.ensure_future(self.get_details_or_create(d))
            #     for d in data["details"]
            # ]
            # subtitles_coroutines = [
            #     asyncio.ensure_future(self.get_subtitles_or_create(s))
            #     for s in data["subtitles"]
            # ]
            # data["details"] = await asyncio.gather(*details_coroutines)
            # data["subtitles"] = await asyncio.gather(*subtitles_coroutines)
            await self.user_history_repo.create(data, session=session)

        except Exception as err:
            logger.error(f"gather_data --> {err}")
        finally:
            return None

    async def add_user_data_to_db(self):
        try:
            with open(SEARCH_HISTORY_PATH, "r", encoding="utf-8") as file:
                user_data = json.load(file)
            async with HTTPClient() as httpClient:
                async with init_db() as session:
                    # tasks = []
                    # for data in user_data[:10]:
                    # tasks.append(
                    #     asyncio.ensure_future(
                    #         self._gather_data_and_ingest(httpClient, data)
                    #     )
                    # )
                    # responses = await asyncio.gather(*tasks)
                    responses = [
                        await self._gather_data_and_ingest(
                            httpClient, data, session=session
                        )
                        for data in tqdm(user_data[:10])
                    ]

            return responses

        except Exception as err:
            logger.error(f"Controller error --> {err}")
