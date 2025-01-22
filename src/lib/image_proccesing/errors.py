import dataclasses


@dataclasses.dataclass
class ImageSaveError(Exception):
    text: str
