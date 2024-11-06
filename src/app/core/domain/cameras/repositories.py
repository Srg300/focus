from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Camera


class CameraRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(
        self,
        id_: int | None = None,
        title: str | None = None,
    ) -> Camera | None:
        stmt = select(Camera)

        if id_ is not None:
            stmt = stmt.where(Camera.id == id_)
        if title is not None:
            stmt = stmt.where(Camera.title == title)

        return (await self._session.scalars(stmt)).one_or_none()
