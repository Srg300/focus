from app.core.domain.cameras.repositories import CameraRepository
from app.db.models import Camera


class CameraGetQuery:
    def __init__(self, repository: CameraRepository) -> None:
        self._repository = repository

    async def execute(self, camera_id: int) -> Camera | None:
        return await self._repository.get(id_=camera_id)
