from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.candidate import CandidateProfile
from app.models.skill import CandidateSkill
from app.models.role import CandidateRole
from app.models.user import User
from app.schemas.candidate import CandidateCreate, CandidateResponse, CandidateSkillCreate, CandidateRoleCreate


router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"],
)


@router.post("/", response_model=CandidateResponse)
def create_candidate(
    candidate_data: CandidateCreate,
    db: Session = Depends(get_db),
):
    try:
        # 1. Check user
        user = db.get(User, candidate_data.user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        # 2. Check existing candidate
        existing_candidate = (
            db.query(CandidateProfile)
            .filter(
                CandidateProfile.user_id == candidate_data.user_id
            )
            .first()
        )

        if existing_candidate:
            raise HTTPException(
                status_code=400,
                detail="Candidate profile already exists for this user",
            )

        # 3. Create candidate
        candidate = CandidateProfile(
            user_id=candidate_data.user_id,
            full_name=candidate_data.full_name,
            years_experience=candidate_data.years_experience,
            summary=candidate_data.summary,
            preferred_location=candidate_data.preferred_location,
            remote_preference=candidate_data.remote_preference,
            min_salary=candidate_data.min_salary,
            max_salary=candidate_data.max_salary,
        )

        db.add(candidate)
        db.flush()

        # 4. Create skills
        for skill_data in candidate_data.skills:
            skill = CandidateSkill(
                candidate_id=candidate.id,
                skill_name=skill_data.skill_name,
                skill_type=skill_data.skill_type,
                proficiency=skill_data.proficiency,
                years_experience=skill_data.years_experience,
            )

            db.add(skill)

        # 5. Create roles
        for role_data in candidate_data.roles:
            role = CandidateRole(
                candidate_id=candidate.id,
                role_name=role_data.role_name,
                priority=role_data.priority,
            )

            db.add(role)

        # 6. Flush so SQLAlchemy knows about everything
        db.flush()

        # 7. Explicitly validate/build response BEFORE commit
        response = CandidateResponse(
            id=candidate.id,
            user_id=candidate.user_id,
            full_name=candidate.full_name,
            years_experience=candidate.years_experience,
            summary=candidate.summary,
            preferred_location=candidate.preferred_location,
            remote_preference=candidate.remote_preference,
            min_salary=candidate.min_salary,
            max_salary=candidate.max_salary,
            skills=[
                CandidateSkillCreate(
                    skill_name=skill.skill_name,
                    skill_type=skill.skill_type,
                    proficiency=skill.proficiency,
                    years_experience=skill.years_experience,
                )
                for skill in candidate.skills
            ],
            roles=[
                CandidateRoleCreate(
                    role_name=role.role_name,
                    priority=role.priority,
                )
                for role in candidate.roles
            ],
        )

        # 8. Only commit AFTER response validation succeeds
        db.commit()

        return response

    except Exception:
        # If anything fails before commit,
        # all pending DB changes are rolled back.
        db.rollback()
        raise