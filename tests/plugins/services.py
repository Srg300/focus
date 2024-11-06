import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.cameras.dto import CameraCreateDTO
from app.core.domain.cameras.repositories import CameraRepository
from app.core.domain.cameras.services import CameraService
from app.db.models import Camera
from lib.db import DBContext


@pytest.fixture
def db_context(session: AsyncSession) -> DBContext:
    return session


@pytest.fixture
def camera_repository(session: AsyncSession) -> CameraRepository:
    return CameraRepository(
        session=session,
    )


@pytest.fixture
def camera_service(
    camera_repository: CameraRepository, db_context: DBContext
) -> CameraService:
    return CameraService(
        repository=camera_repository,
        db_context=db_context,
    )


@pytest.fixture
async def camera(camera_service: CameraService) -> Camera:
    camera = await camera_service.create(
        dto=CameraCreateDTO(
            title=str(uuid.uuid4()),
            url=str(uuid.uuid4()),
        )
    )
    return camera.unwrap()
