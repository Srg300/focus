import dataclasses


@dataclasses.dataclass
class InvalidHttpCameraUrlError(Exception):
    status_code: int
    text: str = ""
