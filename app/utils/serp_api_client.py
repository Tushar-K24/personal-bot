from .http_client import HTTPClient
from ..settings.globals import SERP_API_KEY


class SerpAPI(HTTPClient):
    url: str = "https://serpapi.com/search"
    __api_key: str = SERP_API_KEY

    def __init__(self):
        super().__init__()
        assert self.__api_key != "", f"{self.__class__.__name__}: api key missing"

    async def google_search(
        self, searchText: str, hl: str = "en", gl: str = "us"
    ) -> dict:
        params: dict = {"q": searchText, "hl": hl, "gl": gl, "api_key": self.__api_key}
        return await self.make_request("GET", self.url, params)


client = SerpAPI()
