import asyncio

from result import Err, Ok, Result

from app.core.errors import InvalidHttpCameraUrlError
from app.core.validators import HttpUrlCheckValidator
from app.db.models import Camera
from app.ports.telegram.client import TelegramClient
from lib.image_proccesing.errors import ImageSaveError
from lib.image_proccesing.image_capture import ImageCapture

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


class CameraHttpImageCommand:
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


class CameraRtpsImageCommand:
    def __init__(
        self,
        image_capture: ImageCapture,
    ) -> None:
        self._image_capture = image_capture

    async def execute(self, url: str) -> Result[str, ImageSaveError]:
        return await asyncio.to_thread(self._image_capture.save_image, url)


class CameraRtpsBase64Command:
    def __init__(
        self,
        image_capture: ImageCapture,
        tg_client: TelegramClient,
    ) -> None:
        self._image_capture = image_capture
        self._tg_client = tg_client

    async def execute(self, url: str) -> None:
        # TODO(srg300): доработать. добавить обработку ошибок ТГ.
        image_bytes = await asyncio.to_thread(self._image_capture.get_image_bytes, url)
        if isinstance(image_bytes, Ok):
            await self._tg_client.telegram_send_image(
                chat_id=1234,
                image_bytes=image_bytes.ok_value,
            )
