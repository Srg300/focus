from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import NewType

import httpx
from pydantic import BaseModel

from app.settings import TelegramBotSettings
from lib.settings import get_settings

tg_settings = get_settings(TelegramBotSettings)

TelegramClient = NewType("TelegramClient", httpx.AsyncClient)


class SendData(BaseModel):
    chat_id: int
    message: str


@asynccontextmanager
async def get_http_client(
    settings: TelegramBotSettings,
) -> AsyncIterator[TelegramClient]:
    async with httpx.AsyncClient(
        base_url=settings.url,
        timeout=10.0,
    ) as client:
        yield TelegramClient(client)


async def telegram_send_message(
    chat_id: int, message: str, client: TelegramClient
) -> httpx.Response:
    data = SendData(chat_id=chat_id, message=message)
    client.headers["Authorization"] = f"Bearer {tg_settings.token}"
    response = await client.post(
        f"{tg_settings.url}/sendMessage", json=data.model_dump()
    )
    response.raise_for_status()
    return response
