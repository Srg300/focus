import pydantic
from pydantic import ConfigDict

from app.adapters.api.schema import BaseSchema


class CameraSchema(BaseSchema):
    model_config = ConfigDict(title="Camera")

    id: int
    title: str
    url: str


class CameraCreateSchema(BaseSchema):
    model_config = ConfigDict(title="CameraCreate")

    title: str = pydantic.Field(max_length=255)
    url: str = pydantic.Field()
