import asyncio
from collections.abc import AsyncGenerator

import cv2

from app.settings import AppSettings
from lib.settings import get_settings

app_settings = get_settings(AppSettings)


class VideoStreamCapture:
    async def video_stream(self, url: str) -> AsyncGenerator[bytes, None]:
        cv_capture = cv2.VideoCapture()
        if not cv_capture.open(url):
            return

        try:
            while True:
                ret, frame = cv_capture.read()
                if not ret:
                    break
                ret, jpeg = cv2.imencode(".jpg", frame)
                if not ret:
                    continue
                frame_bytes = jpeg.tobytes()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )
                await asyncio.sleep(0.01)
        finally:
            cv_capture.release()
