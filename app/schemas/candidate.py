from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class CandidateSkillCreate(BaseModel):
    skill_name: str
    skill_type: str | None = None
    proficiency: str | None = None
    years_experience: Decimal | None = None


class CandidateRoleCreate(BaseModel):
    role_name: str
    priority: int = Field(default=1, ge=1)


class CandidateCreate(BaseModel):
    user_id: UUID
    full_name: str
    years_experience: Decimal = Field(ge=0)
    summary: str | None = None
    preferred_location: str | None = None
    remote_preference: bool = False
    min_salary: int | None = None
    max_salary: int | None = None

    skills: list[CandidateSkillCreate] = []
    roles: list[CandidateRoleCreate] = []


class CandidateResponse(BaseModel):
    id: UUID
    user_id: UUID
    full_name: str
    years_experience: Decimal
    summary: str | None
    preferred_location: str | None
    remote_preference: bool
    min_salary: int | None
    max_salary: int | None

    skills: list[CandidateSkillCreate]
    target_roles: list[CandidateRoleCreate]

    model_config = {
        "from_attributes": True
    }