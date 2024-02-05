from serpapi import GoogleSearch
from ..settings.globals import SERP_API_KEY


class SerpAPI:
    __api_key: str = SERP_API_KEY
    google_domain: str = "google.com"

    def __init__(self):
        assert self.__api_key != "", f"{self.__class__.__name__}: api key missing"

    def google_search(
        self, searchText: str, location: str = "India", hl: str = "en", gl: str = "us"
    ) -> dict:
        params: dict = {
            "q": searchText,
            "location": location,
            "hl": hl,
            "gl": gl,
            "google_domain": self.google_domain,
            "api_key": self.__api_key,
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results


client = SerpAPI()
