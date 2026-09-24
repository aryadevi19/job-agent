import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    skill_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    skill_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    proficiency: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    years_experience: Mapped[Decimal | None] = mapped_column(
        Numeric(4, 2),
        nullable=True,
    )

    candidate = relationship(
        "CandidateProfile",
        back_populates="skills",
    )