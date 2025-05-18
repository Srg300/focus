from pydantic import Field

from lib.dto import BaseDTO


class CameraCreateDTO(BaseDTO):
    title: str
    host: str
    protocol: str = Field(default="http")
    login: str | None = None
    password: str | None = None
    path: str | None = None
