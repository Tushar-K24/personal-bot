import aiohttp
from async_lru import alru_cache
from asyncio import Semaphore

from app.core.config import CONCURRENT_REQUESTS_LIMIT


class HTTPClient:
    semaphores = Semaphore(CONCURRENT_REQUESTS_LIMIT)

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        self._method_map: dict = {
            "GET": self._session.get,
            "POST": self._session.post,
            "PUT": self._session.put,
            "PATCH": self._session.patch,
            "DELETE": self._session.delete,
        }
        self._valid_methods: set = set(self._method_map.keys())
        return self

    async def __aexit__(self, *args):
        await self._session.close()

    @alru_cache(maxsize=32)
    async def make_request(
        self,
        method: str,
        url: str,
        query_param: dict = None,
        headers: dict = None,
        body: dict = None,
        **kwargs,
    ):
        assert (
            method in self._valid_methods
        ), f"{self.__class__.__name__}: Invalid method"
        http_method = self._method_map[method]
        try:
            async with self.semaphores:
                async with http_method(
                    url, params=query_param, headers=headers, data=body, **kwargs
                ) as response:
                    if response.status != 200:
                        raise Exception(
                            f"Request failed with status {response.status} for url {url}"
                        )
                    content_type = response.headers.get("Content-Type", "")
                    if "json" in content_type:
                        data = await response.json()
                    elif "text" in content_type:
                        data = await response.text()
                    else:
                        data = await response.read()
                    kwargs["data"] = data
                    return kwargs
        except Exception as err:
            raise Exception(f"{self.__class__.__name__} --> {err}")
