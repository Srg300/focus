import aioinject
from cv2 import VideoCapture

from lib.opencv.image_capture import ImageCapture
from lib.types import Providers

providers: Providers = [
    aioinject.Scoped(ImageCapture),
    aioinject.Scoped(VideoCapture),
]
