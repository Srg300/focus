from collections.abc import Iterable
from typing import Any

import aioinject

from .httpx_client import HttpxClient, get_http_client

providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Singleton(get_http_client, type_=HttpxClient),
]
