from pydantic import ConfigDict, Field

from app.adapters.api.schema import BaseSchema


class CameraSchema(BaseSchema):
    model_config = ConfigDict(title="Camera")

    id: int
    title: str
    url: str


class CameraCreateSchema(BaseSchema):
    model_config = ConfigDict(title="CameraCreate")

    title: str = Field(max_length=255)
    url: str


class CameraGetImageSchema(BaseSchema):
    url: str


class SaveImageSchema(BaseSchema):
    name: str


class RtpsCameraSchema(BaseSchema):
    login: str = Field(default="")
    password: str = Field(default="")
    host: str
    port: int = Field(gt=0)
    resource_path: str = Field(default="")
