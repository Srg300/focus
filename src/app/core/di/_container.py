import functools
import itertools
from collections.abc import Iterable
from typing import Any

import aioinject
from aioinject import Provider

from app import connectors
from app.core.validators import HttpUrlCheckValidator
from app.ports.telegram.client import TelegramClient

from ._modules import cameras, database, opencv

modules: Iterable[Iterable[Provider[Any]]] = [
    database.providers,
    cameras.providers,
    opencv.providers,
    connectors.providers,
]


@functools.cache
def create_container() -> aioinject.Container:
    container = aioinject.Container()

    for provider in itertools.chain.from_iterable(modules):
        container.register(provider)

    container.register(aioinject.Scoped(HttpUrlCheckValidator))
    container.register(aioinject.Scoped(TelegramClient))

    return container
