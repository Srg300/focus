import uuid

from result import Err, Ok
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.cameras.dto import CameraCreateDTO
from app.core.domain.cameras.errors import CameraAlreadyExistsError
from app.core.domain.cameras.repositories import CameraRepository
from app.core.domain.cameras.services import CameraService
from app.db.models import Camera


async def test_create(
    session: AsyncSession,
    camera_service: CameraService,
) -> None:
    camera = await camera_service.create(
        dto=CameraCreateDTO(
            title=str(uuid.uuid4()),
            host=str(uuid.uuid4()),
        )
    )
    assert isinstance(camera, Ok)
    assert await session.get(Camera, camera.ok_value.id)


async def test_create_duplicate_title(
    camera: Camera,
    camera_service: CameraService,
) -> None:
    result = await camera_service.create(
        dto=CameraCreateDTO(title=camera.title, host=camera.host)
    )
    assert isinstance(result, Err)
    assert isinstance(result.err_value, CameraAlreadyExistsError)


async def test_get_one(
    camera: Camera,
    camera_repository: CameraRepository,
) -> None:
    camera_in_db = await camera_repository.get(id_=camera.id)
    assert camera is camera_in_db


async def test_get_one_not_found(
    camera_repository: CameraRepository,
) -> None:
    assert await camera_repository.get(id_=1) is None
