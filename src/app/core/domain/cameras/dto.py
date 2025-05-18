from app.core.security import get_password_hash
from lib.dto import BaseDTO


class CameraCreateDTO(BaseDTO):
    title: str
    url: str
    login: str | None = None
    password: str | None = None

    @property
    def hashed_password(self) -> str | None:
        return get_password_hash(password=self.password) if self.password else None
