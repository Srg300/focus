import uuid
from http import HTTPStatus

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Camera


async def test_base_case(
    http_client: httpx.AsyncClient,
    session: AsyncSession,
) -> None:
    title = str(uuid.uuid4())
    host = str(uuid.uuid4())
    response = await http_client.post(
        url="/cameras", json={"title": title, "host": host}
    )
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json["title"] == title
    assert await session.get(Camera, response_json["id"])


async def test_duplicate_title(
    http_client: httpx.AsyncClient,
    camera: Camera,
) -> None:
    response = await http_client.post(
        url="/cameras", json={"title": camera.title, "host": camera.host}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
