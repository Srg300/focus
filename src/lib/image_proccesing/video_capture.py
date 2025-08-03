import asyncio
import threading
from collections.abc import AsyncGenerator

import cv2

from app.settings import AppSettings
from lib.settings import get_settings

app_settings = get_settings(AppSettings)



class Camera:

    def __init__(self) -> None:

        self.cap = cv2.VideoCapture()
        self.lock = threading.Lock()

    def get_frame(self, url: str) -> bytes:
        with self.lock:
            self.cap.open(url)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            ret, frame = self.cap.read()
            if not ret:
                return b""

            params = [cv2.IMWRITE_JPEG_QUALITY, 70]
            ret, jpeg = cv2.imencode(".jpg", frame, params=params)
            if not ret:
                return b""

            return jpeg.tobytes()

    def release(self) -> None:

        with self.lock:
            if self.cap.isOpened():
                self.cap.release()


class VideoStreamCapture:
    def __init__(self, camera: Camera) -> None:
        self.camera = camera

    async def video_stream(self, url: str) -> AsyncGenerator[bytes, None]:
        while True:
            frame = self.camera.get_frame(url=url)
            if frame:
                yield (b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
            else:
                break
            await asyncio.sleep(0)

    async def video_stream_(self, url: str) -> AsyncGenerator[bytes, None]:
        cv_capture = cv2.VideoCapture()
        cv_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cv_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if not cv_capture.open(url):
            return

        try:
            while True:
                ret, frame = cv_capture.read()
                if not ret:
                    break

                params = [cv2.IMWRITE_JPEG_QUALITY, 70]
                ret, webp = cv2.imencode(".png", frame, params=params)
                if not ret:
                    continue

                frame_bytes = webp.tobytes()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )
                await asyncio.sleep(0.1)
        finally:
            cv_capture.release()
