import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    __table_args__ = (
        UniqueConstraint(
            "source",
            "external_id",
            name="uq_job_source_external_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    external_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    remote: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    salary_min: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    salary_max: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    job_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    posted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
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

    requirements = relationship(
        "JobRequirement",
        back_populates="job",
        uselist=False,
        cascade="all, delete-orphan",
    )

    matches = relationship(
        "JobMatch",
        back_populates="job",
        cascade="all, delete-orphan",
    )