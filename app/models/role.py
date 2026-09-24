import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CandidateRole(Base):
    __tablename__ = "candidate_roles"

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

    role_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    candidate = relationship(
        "CandidateProfile",
        back_populates="roles",
    )