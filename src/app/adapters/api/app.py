import contextlib
from collections.abc import AsyncIterator, Iterable

from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.api import cameras
from app.core.di import create_container
from app.settings import AppSettings
from lib.settings import get_settings

_routers: Iterable[APIRouter] = [
    cameras.router,
]


def create_app() -> FastAPI:
    container = create_container()

    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield
        await container.close()

    app = FastAPI(lifespan=lifespan)
    setup_dishka(container, app)

    app_settings = get_settings(AppSettings)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_allow_origins,
        allow_methods=app_settings.cors_allow_methods,
        allow_headers=app_settings.cors_allow_headers,
    )

    for router in _routers:
        app.include_router(router)

    @app.get("/health")
    async def healthcheck() -> None:
        return None

    return app
