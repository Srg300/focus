from dishka import Provider, Scope, provide

from app.core.domain.cameras.commands import (
    CameraCreateCommand,
    CameraHttpImageCommand,
    CameraRtpsBase64Command,
    CameraRtpsImageCommand,
)
from app.core.domain.cameras.queries import CameraGetQuery
from app.core.domain.cameras.repositories import CameraRepository
from app.core.domain.cameras.services import CameraService


class CamerasProvider(Provider):
    scope = Scope.REQUEST

    camera_repo = provide(CameraRepository, scope=Scope.REQUEST)
    camera_service = provide(CameraService, scope=Scope.REQUEST)
    camera_get_query = provide(CameraGetQuery, scope=Scope.REQUEST)
    camera_create_cmd = provide(CameraCreateCommand, scope=Scope.REQUEST)
    camera_http_cmd = provide(CameraHttpImageCommand, scope=Scope.REQUEST)
    camera_rtps_cmd = provide(CameraRtpsImageCommand, scope=Scope.REQUEST)
    camera_base64_cmd = provide(CameraRtpsBase64Command, scope=Scope.REQUEST)
