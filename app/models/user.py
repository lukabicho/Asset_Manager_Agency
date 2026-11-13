"""This File defines how data is stored in a database"""
import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4,nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] =mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

