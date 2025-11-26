from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ShortURL(Base):
    """ """

    __tablename__ = "short_urls"

    slug: Mapped[str] = mapped_column(String(length=6), primary_key=True)
    long_url: Mapped[str] = mapped_column(String(length=2048))
    creation_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    click_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now,
        nullable=False,
    )
    last_accessed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
