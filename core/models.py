"""
SQLAlchemy ORM models for ViralClip SaaS.
Tables: User, VerificationToken, Job
"""
from datetime import datetime, timedelta
from sqlalchemy import (
    String, Integer, Boolean, DateTime, Text, ForeignKey, Float, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
import secrets


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    credits: Mapped[int] = mapped_column(Integer, default=50)  # 50 free credits on signup
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    jobs: Mapped[list["Job"]] = relationship("Job", back_populates="user", lazy="selectin")
    tokens: Mapped[list["VerificationToken"]] = relationship("VerificationToken", back_populates="user", lazy="selectin")


class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    purpose: Mapped[str] = mapped_column(String(50), default="login")  # "login" or "register"
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    user: Mapped[User | None] = relationship("User", back_populates="tokens")

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(48)

    @staticmethod
    def default_expiry() -> datetime:
        return datetime.utcnow() + timedelta(minutes=30)


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    celery_task_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    engine: Mapped[str] = mapped_column(String(50), default="auto")
    num_clips: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="PENDING")  # PENDING, STARTED, SUCCESS, FAILURE
    progress: Mapped[float] = mapped_column(Float, default=0.0)  # 0.0 to 100.0
    current_step: Mapped[str | None] = mapped_column(String(100), nullable=True)
    result_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    credits_used: Mapped[int] = mapped_column(Integer, default=10)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="jobs")
