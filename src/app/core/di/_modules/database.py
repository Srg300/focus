from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.db import async_session_factory
from app.db import engine as app_engine
from lib.db import DBContext


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        try:
            yield app_engine
        finally:
            await app_engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def session(self, _: AsyncEngine) -> AsyncIterator[AsyncSession]:
        async with async_session_factory.begin() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def db_context(self, session: AsyncSession) -> DBContext:
        return session
