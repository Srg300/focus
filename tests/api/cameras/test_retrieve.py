import uuid
from http import HTTPStatus

import httpx
import pytest

from app.core.domain.cameras.dto import CameraCreateDTO
from app.core.domain.cameras.services import CameraService

pytestmark = [pytest.mark.usefixtures("session")]


async def test_not_found(
    http_client: httpx.AsyncClient,
) -> None:
    response = await http_client.get("/cameras/1")
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_base_case(
    http_client: httpx.AsyncClient,
    camera_service: CameraService,
) -> None:
    camera = (
        await camera_service.create(
            CameraCreateDTO(title=str(uuid.uuid4()), url=str(uuid.uuid4()))
        )
    ).unwrap()

    response = await http_client.get(f"/cameras/{camera.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": camera.id,
        "title": camera.title,
        "url": camera.url,
    }
