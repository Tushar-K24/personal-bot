import requests


class HTTPClient:
    def __init__(self) -> None:
        self._method_map: dict = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "PATCH": requests.patch,
            "DELETE": requests.delete,
        }
        self._valid_methods: set = set(self._method_map.keys())

    def make_request(self, method: str, url: str, **kwargs):
        assert (
            method in self._valid_methods
        ), f"{self.__class__.__name__}: Invalid method"
        http_method = self._method_map[method]
        return http_method(url=url, **kwargs)


client = HTTPClient()
