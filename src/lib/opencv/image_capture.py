from cv2 import VideoCapture, imwrite

from app.settings import AppSettings
from lib.settings import get_settings
from lib.time import utc_now

app_settings = get_settings(AppSettings)


class ImageCapture:
    def __init__(
        self,
        cv_capture: VideoCapture,
    ) -> None:
        self._cv_capture = cv_capture

    def execute(self, url: str) -> str | None:
        capture = self._cv_capture
        capture.open(url)
        ret, frame = capture.read()
        if ret:
            file_name = utc_now().strftime("%Y%m%d-%H%M%S")
            imwrite(f"{app_settings.image_path}/{file_name}.png", frame)
            return file_name
        return None
