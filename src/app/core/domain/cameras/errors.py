import dataclasses


@dataclasses.dataclass
class CameraAlreadyExistsError(Exception): ...
