import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    years_experience: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    preferred_location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    remote_preference: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    min_salary: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    max_salary: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="candidate_profile",
    )

    skills = relationship(
        "CandidateSkill",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )

    roles = relationship(
        "CandidateRole",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )

    matches = relationship(
        "JobMatch",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )