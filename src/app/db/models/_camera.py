from sqlalchemy import String, Text, true
from sqlalchemy.orm import Mapped, mapped_column

from app.db._base import Base


class Camera(Base):
    __tablename__ = "camera"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    url: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())
