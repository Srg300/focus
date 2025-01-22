import base64

from cv2 import VideoCapture, imencode, imwrite
from result import Err, Ok, Result

from app.settings import AppSettings
from lib.settings import get_settings
from lib.time import utc_now

from .errors import ImageSaveError

app_settings = get_settings(AppSettings)


class ImageCapture:
    def __init__(
        self,
        cv_capture: VideoCapture,
    ) -> None:
        self._cv_capture = cv_capture

    def save_image(self, url: str) -> Result[str, ImageSaveError]:
        if not self._cv_capture.open(url):
            return Err(ImageSaveError("Failed to open RTSP stream"))

        ret, frame = self._cv_capture.read()
        self._cv_capture.release()

        if ret:
            file_name = utc_now().strftime("%Y%m%d-%H%M%S")
            imwrite(f"{app_settings.image_path}/{file_name}.png", frame)
            return Ok(file_name)
        return Err(ImageSaveError("Failed to read frame from RTSP stream"))

    def get_image_base64(self, url: str) -> Result[str, ImageSaveError]:
        if not self._cv_capture.open(url):
            return Err(ImageSaveError("Failed to open RTSP stream"))

        ret, frame = self._cv_capture.read()
        self._cv_capture.release()

        if ret:
            _, buffer = imencode(".png", frame)
            img_base64 = base64.b64encode(buffer).decode("utf-8")
            return Ok(img_base64)
        return Err(ImageSaveError("Failed to read frame from RTSP stream"))

    def get_image_bytes(self, url: str) -> Result[bytes, ImageSaveError]:
        if not self._cv_capture.open(url):
            return Err(ImageSaveError("Failed to open RTSP stream"))
        ret, frame = self._cv_capture.read()
        self._cv_capture.release()
        if not ret:
            return Err(ImageSaveError("Failed to read frame from RTSP stream"))
        is_success, buffer = imencode(".png", frame)
        if not is_success:
            return Err(ImageSaveError("Failed to encode image to PNG format"))

        return Ok(buffer.tobytes())
