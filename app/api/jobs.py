from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
):
    try:
        # 1. Check whether this job already exists
        existing_job = (
            db.query(Job)
            .filter(
                Job.source == job_data.source,
                Job.external_id == job_data.external_id,
            )
            .first()
        )

        if existing_job:
            raise HTTPException(
                status_code=409,
                detail="Job already exists for this source",
            )

        # 2. Create Job object
        job = Job(
            external_id=job_data.external_id,
            source=job_data.source,
            title=job_data.title,
            company_name=job_data.company_name,
            description=job_data.description,
            location=job_data.location,
            remote=job_data.remote,
            employment_type=job_data.employment_type,
            salary_min=job_data.salary_min,
            salary_max=job_data.salary_max,
            job_url=str(job_data.job_url),
            posted_at=job_data.posted_at,
        )

        db.add(job)

        # Generate ID / check DB constraints
        db.flush()

        # 3. Validate response BEFORE commit
        response = JobResponse.model_validate(job)

        # 4. Commit only after validation succeeds
        db.commit()

        return response

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise