from datetime import datetime, timezone
from typing import TypeVar, Generic
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped


M = TypeVar("M", bound="BaseModel")

class BaseModel(DeclarativeBase, Generic[M]):

    __abstract__ = True

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)

    # Timestamp: Record creation time (default: current UTC time)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Timestamp: Record last update time (auto-updated on modification)
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Timestamp: Record inactivation time
    inactivated_at: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=True
    )

__all__ = ["BaseModel"]
