from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import NewType

import httpx

HttpxClient = NewType("HttpxClient", httpx.AsyncClient)


@asynccontextmanager
async def get_http_client() -> AsyncIterator[HttpxClient]:
    async with httpx.AsyncClient() as client:
        yield HttpxClient(client)
