import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class JobRequirement(Base):
    __tablename__ = "job_requirements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    required_skills: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    preferred_skills: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    min_experience: Mapped[Decimal | None] = mapped_column(
        Numeric(4, 2),
        nullable=True,
    )

    education: Mapped[list] = mapped_column(
        JSONB,
        nullable=True,
    )

    required_keywords: Mapped[list] = mapped_column(
        JSONB,
        nullable=True,
    )

    responsibilities: Mapped[list] = mapped_column(
        JSONB,
        nullable=True,
    )

    extracted_by: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    extraction_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
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

    job = relationship(
        "Job",
        back_populates="requirements",
    )