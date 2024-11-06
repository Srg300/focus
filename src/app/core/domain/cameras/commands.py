from result import Result

from app.db.models import Camera

from .dto import CameraCreateDTO
from .errors import CameraAlreadyExistsError
from .services import CameraService


class CameraCreateCommand:
    def __init__(
        self,
        camera_service: CameraService,
    ) -> None:
        self._camera_service = camera_service

    async def execute(
        self, dto: CameraCreateDTO
    ) -> Result[Camera, CameraAlreadyExistsError]:
        return await self._camera_service.create(dto=dto)
