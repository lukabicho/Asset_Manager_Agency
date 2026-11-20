from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.database.session import Base
"""imports User and Project only when static type checker(PyCharm) analyze the file. at runtime, Python skips this block"""
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project

class Agency(Base):
    """SQLAlchemy model for creating agency table"""
    __tablename__ = "agencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    """Bidirectional ORM relationship to the owning `User` and 'Project' instances in this agency"""
    # owner: Mapped["User"] = relationship("User", back_populates="agencies")
    # projects: Mapped[list["Project"]] = relationship(back_populates="agency", cascade="all, delete-orphan", passive_deletes=True)