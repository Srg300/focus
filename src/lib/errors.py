import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class CameraNotAvailableError:
    message: str = "Camera is not available"


@dataclasses.dataclass(frozen=True, slots=True)
class CameraTimeoutError: ...
