from sqlalchemy import String, true
from sqlalchemy.orm import Mapped, mapped_column

from app.db._base import Base


class Camera(Base):
    __tablename__ = "camera"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    protocol: Mapped[str] = mapped_column(String(20))
    host: Mapped[str] = mapped_column(String(255))
    login: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())
