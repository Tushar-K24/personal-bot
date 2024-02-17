import json
import asyncio

from ...settings.globals import SEARCH_HISTORY_PATH
from ...utils.http_client import HTTPClient
from ...core.logger import logger


async def add_user_data_to_db():
    try:
        with open(SEARCH_HISTORY_PATH, "r", encoding="utf-8") as file:
            user_data = json.load(file)
        tasks = []
        async with HTTPClient() as httpClient:
            for data in user_data["Browser History"][:100]:
                tasks.append(
                    asyncio.ensure_future(httpClient.make_request("GET", data["url"]))
                )
            responses = await asyncio.gather(*tasks)
        return responses
    except Exception as err:
        logger.error(f"Controller error --> {err}")
