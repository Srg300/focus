from cv2 import VideoCapture, imwrite
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
        capture = self._cv_capture
        capture.open(url)
        ret, frame = capture.read()
        if ret:
            file_name = utc_now().strftime("%Y%m%d-%H%M%S")
            imwrite(f"{app_settings.image_path}/{file_name}.png", frame)
            return Ok(file_name)
        return Err(ImageSaveError())
