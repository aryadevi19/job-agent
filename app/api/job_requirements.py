from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.job_extractor import extract_job_requirements
from app.core.database import get_db
from app.models.job import Job
from app.models.job_requirement import JobRequirement
from app.schemas.job_requirement import JobRequirementResponse


router = APIRouter(
    prefix="/jobs",
    tags=["Job Requirements"],
)


@router.post(
    "/{job_id}/extract-requirements",
    response_model=JobRequirementResponse,
)
def extract_requirements(
    job_id: str,
    db: Session = Depends(get_db),
):
    try:
        # 1. Find the job
        job = db.get(Job, job_id)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found",
            )

        # 2. Check whether requirements already exist
        existing_requirements = (
            db.query(JobRequirement)
            .filter(JobRequirement.job_id == job.id)
            .first()
        )

        if existing_requirements:
            raise HTTPException(
                status_code=409,
                detail="Job requirements already extracted",
            )

        # 3. Ask the LLM to extract requirements
        requirements_data = extract_job_requirements(
            title=job.title,
            description=job.description,
        )

        # 4. Create database object
        requirements = JobRequirement(
            job_id=job.id,
            required_skills=requirements_data.required_skills,
            preferred_skills=requirements_data.preferred_skills,
            min_experience=requirements_data.min_experience,
            education=requirements_data.education,
            required_keywords=requirements_data.required_keywords,
            responsibilities=requirements_data.responsibilities,
            extracted_by="gemini",
            extraction_version="v1",
        )

        db.add(requirements)

        # 5. Flush → detect DB constraint errors
        db.flush()

        # 6. Validate response BEFORE commit
        response = JobRequirementResponse.model_validate(
            requirements
        )

        # 7. Commit only after validation
        db.commit()

        return response

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise