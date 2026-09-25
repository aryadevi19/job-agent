from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class JobRequirementCreate(BaseModel):
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)

    min_experience: Decimal | None = None

    education: list[str] = Field(default_factory=list)

    required_keywords: list[str] = Field(default_factory=list)

    responsibilities: list[str] = Field(default_factory=list)


class JobRequirementResponse(BaseModel):
    id: UUID
    job_id: UUID

    required_skills: list[str]
    preferred_skills: list[str]

    min_experience: Decimal | None

    education: list[str]
    required_keywords: list[str]
    responsibilities: list[str]

    extracted_by: str
    extraction_version: str

    model_config = {
        "from_attributes": True
    }