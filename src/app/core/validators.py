import http

from httpx import Response
from result import Err, Ok, Result

from app.connectors.httpx_client import HttpxClient


class HttpUrlCheckValidator:
    def __init__(self, http_client: HttpxClient) -> None:
        self._http_client = http_client

    async def __call__(self, url: str) -> Result[None, Response]:
        response = await self._http_client.get(url)
        if response.status_code != http.HTTPStatus.OK:
            return Err(response)
        return Ok(None)
