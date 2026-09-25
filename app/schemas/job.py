from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class JobCreate(BaseModel):
    external_id: str
    source: str
    title: str
    company_name: str
    description: str

    location: str | None = None
    remote: bool = False
    employment_type: str | None = None

    salary_min: int | None = None
    salary_max: int | None = None

    job_url: HttpUrl

    posted_at: datetime | None = None


class JobResponse(BaseModel):
    id: UUID
    external_id: str
    source: str
    title: str
    company_name: str
    description: str

    location: str | None
    remote: bool
    employment_type: str | None

    salary_min: int | None
    salary_max: int | None

    job_url: str

    posted_at: datetime | None
    discovered_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }