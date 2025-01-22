import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class CameraAvailableError:
    message: str = "Camera is not available"


@dataclasses.dataclass(frozen=True, slots=True)
class CameraTimeoutError: ...
