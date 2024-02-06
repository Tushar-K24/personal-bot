from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator
from sqlalchemy.engine.url import URL
from starlette.datastructures import Secret


class DatabaseURL(BaseModel):
    drivername: str
    host: str = "localhost"
    port: Optional[Union[str, int]] = None
    username: Optional[str] = None
    password: Optional[Union[str, Secret]] = None
    database: str
    url: Optional[URL] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True, allow_population_by_alias=True
    )

    @field_validator("url")
    def build_url(cls, v: Any, info: ValidationInfo):
        if isinstance(v, URL):
            return v
        args = {k: str(v) for k, v in info.data.items() if v is not None}
        print(args)
        return URL(**args)
