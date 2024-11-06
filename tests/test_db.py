from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Camera


async def test_cameras_db(session: AsyncSession) -> None:
    camera_count = 10
    session.add_all([Camera(title=f"{i}", url="url") for i in range(camera_count)])
    await session.flush()

    cameras = (await session.scalars(select(Camera))).all()
    assert len(cameras) == camera_count
