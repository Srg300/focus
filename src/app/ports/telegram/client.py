from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import NewType

import httpx
from pydantic import BaseModel

from app.settings import TelegramBotSettings
from lib.settings import get_settings

tg_settings = get_settings(TelegramBotSettings)

TelegramHttpClient = NewType("TelegramHttpClient", httpx.AsyncClient)


class SendData(BaseModel):
    chat_id: int
    message: str


class FileData(BaseModel):
    photo: tuple[str, bytes, str]


class SendFile(BaseModel):
    chat_id: int
    files: FileData


@asynccontextmanager
async def get_http_client(
    settings: TelegramBotSettings,
) -> AsyncIterator[TelegramHttpClient]:
    async with httpx.AsyncClient(
        base_url=settings.url,
        timeout=10.0,
    ) as client:
        yield TelegramHttpClient(client)


class TelegramClient:
    def __init__(
        self,
        client: TelegramHttpClient,
    ) -> None:
        self._client = client

    async def telegram_send_message(
        self,
        chat_id: int,
        message: str,
    ) -> httpx.Response:
        data = SendData(chat_id=chat_id, message=message)
        self._client.headers["Authorization"] = f"Bearer {tg_settings.token}"
        response = await self._client.post(
            f"{tg_settings.url}/sendMessage", json=data.model_dump()
        )
        response.raise_for_status()
        return response

    async def telegram_send_image(
        self, chat_id: int, image_bytes: bytes, name: str = "image.png"
    ) -> httpx.Response:
        data = SendFile(
            chat_id=chat_id, files=FileData(photo=(name, image_bytes, "image/png"))
        )
        self._client.headers["Authorization"] = f"Bearer {tg_settings.token}"
        response = await self._client.post(
            f"{tg_settings.url}/sendPhoto", json=data.model_dump()
        )
        response.raise_for_status()
        return response
