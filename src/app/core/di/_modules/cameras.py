import aioinject

from app.core.domain.cameras.commands import (
    CameraCreateCommand,
    CameraHttpImageCommand,
    CameraRtpsBase64Command,
    CameraRtpsImageCommand,
)
from app.core.domain.cameras.queries import CameraGetQuery
from app.core.domain.cameras.repositories import CameraRepository
from app.core.domain.cameras.services import CameraService
from lib.types import Providers

providers: Providers = [
    aioinject.Scoped(CameraRepository),
    aioinject.Scoped(CameraService),
    aioinject.Scoped(CameraGetQuery),
    aioinject.Scoped(CameraCreateCommand),
    aioinject.Scoped(CameraHttpImageCommand),
    aioinject.Scoped(CameraRtpsImageCommand),
    aioinject.Scoped(CameraRtpsBase64Command),
]
