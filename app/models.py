from sqlalchemy import Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db_session import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    priority: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="media",
    )
    created_at: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )