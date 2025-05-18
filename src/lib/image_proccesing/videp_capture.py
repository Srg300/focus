import asyncio
from collections.abc import AsyncGenerator

from cv2 import VideoCapture, imencode

from app.settings import AppSettings
from lib.settings import get_settings

app_settings = get_settings(AppSettings)


class VideoStreamCapture:
    def __init__(
        self,
        cv_capture: VideoCapture,
    ) -> None:
        self._cv_capture = cv_capture

    async def video_stream(self, url: str) -> AsyncGenerator[bytes, None]:
        if not self._cv_capture.open(url):
            return

        try:
            while True:
                ret, frame = self._cv_capture.read()
                if not ret:
                    break
                ret, jpeg = imencode(".jpg", frame)
                if not ret:
                    continue
                frame_bytes = jpeg.tobytes()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )
                await asyncio.sleep(0.01)
        finally:
            self._cv_capture.release()
