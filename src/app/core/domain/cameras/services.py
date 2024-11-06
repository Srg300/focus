from result import Err, Ok, Result

from app.db.models import Camera
from lib.db import DBContext

from .dto import CameraCreateDTO
from .errors import CameraAlreadyExistsError
from .repositories import CameraRepository


class CameraService:
    def __init__(
        self,
        repository: CameraRepository,
        db_context: DBContext,
    ) -> None:
        self._repository = repository
        self._db_context = db_context

    async def create(
        self,
        dto: CameraCreateDTO,
    ) -> Result[Camera, CameraAlreadyExistsError]:
        if await self._repository.get(title=dto.title) is not None:
            return Err(CameraAlreadyExistsError())

        camera = Camera(
            title=dto.title,
            url=dto.url,
        )
        self._db_context.add(camera)
        await self._db_context.flush()
        return Ok(camera)
