from collections.abc import AsyncIterator
from functools import lru_cache

from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
    provide,
)

from app.connectors.httpx_client import HttpxClient, get_http_client
from app.core.validators import HttpUrlCheckValidator
from app.ports.telegram.client import TelegramClient, TelegramHttpClient

from ._modules.cameras import CamerasProvider
from ._modules.database import DatabaseProvider
from ._modules.opencv import OpenCvProvider


class HttpxClientProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def httpx_client(self) -> AsyncIterator[HttpxClient]:
        async with get_http_client() as client:
            yield client

    @provide(scope=Scope.REQUEST)
    async def telegram_http_client(
        self, http_client: HttpxClient
    ) -> AsyncIterator[TelegramHttpClient]:
        yield TelegramHttpClient(http_client)


class TelegramClientProvider(Provider):
    scope = Scope.REQUEST  # или Scope.APP, если клиент должен быть singleton

    @provide
    def telegram_client(self, client: TelegramHttpClient) -> TelegramClient:
        return TelegramClient(client)


class ValidatorsProvider(Provider):
    scope = Scope.REQUEST
    url_validator = provide(HttpUrlCheckValidator)


@lru_cache
def create_container() -> AsyncContainer:
    return make_async_container(
        DatabaseProvider(),
        CamerasProvider(),
        OpenCvProvider(),
        ValidatorsProvider(),
        HttpxClientProvider(),
        TelegramClientProvider(),
    )
