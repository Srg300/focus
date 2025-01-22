import aioinject
from cv2 import VideoCapture

from lib.image_proccesing.image_capture import ImageCapture
from lib.types import Providers

providers: Providers = [
    aioinject.Scoped(ImageCapture),
    aioinject.Scoped(VideoCapture),
]
