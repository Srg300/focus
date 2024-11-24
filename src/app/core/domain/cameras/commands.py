import asyncio

from result import Err, Result

from app.core.errors import InvalidHttpCameraUrlError
from app.core.validators import HttpUrlCheckValidator
from app.db.models import Camera
from lib.opencv.errors import ImageSaveError
from lib.opencv.image_capture import ImageCapture

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


class CameraHttpGetImageCommand:
    def __init__(
        self,
        image_capture: ImageCapture,
        validator: HttpUrlCheckValidator,
    ) -> None:
        self._image_capture = image_capture
        self._validator = validator

    async def execute(
        self, url: str
    ) -> Result[str, InvalidHttpCameraUrlError | ImageSaveError]:
        error = await self._validator(url=url)
        if isinstance(error, Err):
            return Err(
                InvalidHttpCameraUrlError(
                    status_code=error.err_value.status_code,
                    text=f"Error by status code {error.err_value.status_code}",
                )
            )

        return await asyncio.to_thread(self._image_capture.save_image, url)
