from cv2 import VideoCapture
from dishka import Provider, Scope, provide

from lib.image_proccesing.image_capture import ImageCapture
from lib.image_proccesing.video_capture import VideoStreamCapture


class OpenCvProvider(Provider):
    scope = Scope.REQUEST

    image_capture = provide(ImageCapture, scope=Scope.REQUEST)

    video_stream_cap = provide(VideoStreamCapture, scope=Scope.REQUEST)

    @provide
    def video_capture(self) -> VideoCapture:
        return VideoCapture(0)
