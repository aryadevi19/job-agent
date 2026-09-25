from decimal import Decimal
from typing import Any


def normalize_skill(skill: str) -> str:
    """Normalize skill names for comparison."""
    return skill.strip().lower()


def calculate_skill_score(
    candidate_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
) -> tuple[float, list[str], list[str]]:
    """
    Calculate skill match score.

    Required skills have more importance than preferred skills.
    """

    candidate_skill_set = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    required = {
        normalize_skill(skill)
        for skill in required_skills
    }

    preferred = {
        normalize_skill(skill)
        for skill in preferred_skills
    }

    matched_required = candidate_skill_set.intersection(required)
    matched_preferred = candidate_skill_set.intersection(preferred)

    missing_required = required - candidate_skill_set

    # Required skills = 80% of skill score
    # Preferred skills = 20% of skill score

    if required:
        required_score = (
            len(matched_required) / len(required)
        ) * 80
    else:
        required_score = 80

    if preferred:
        preferred_score = (
            len(matched_preferred) / len(preferred)
        ) * 20
    else:
        preferred_score = 20

    skill_score = required_score + preferred_score

    matched_skills = sorted(
        matched_required | matched_preferred
    )

    missing_skills = sorted(missing_required)

    return (
        round(skill_score, 2),
        matched_skills,
        missing_skills,
    )


def calculate_experience_score(
    candidate_experience: Decimal | float,
    required_experience: Decimal | float | None,
) -> float:
    """
    Calculate experience alignment score.
    """

    if required_experience is None:
        return 100.0

    candidate_experience = float(candidate_experience)
    required_experience = float(required_experience)

    if candidate_experience >= required_experience:
        return 100.0

    if required_experience == 0:
        return 100.0

    score = (
        candidate_experience / required_experience
    ) * 100

    return round(min(score, 100), 2)


def calculate_location_score(
    candidate_location: str | None,
    job_location: str | None,
    candidate_remote_preference: bool,
    job_remote: bool,
) -> float:
    """
    Calculate location compatibility.
    """

    if job_remote and candidate_remote_preference:
        return 100.0

    if not candidate_location or not job_location:
        return 50.0

    candidate_location = candidate_location.strip().lower()
    job_location = job_location.strip().lower()

    if candidate_location == job_location:
        return 100.0

    if candidate_remote_preference and job_remote:
        return 100.0

    return 0.0


def calculate_role_score(
    candidate_roles: list[str],
    job_title: str,
) -> float:
    """
    Basic role relevance score.

    This is intentionally simple for V1.
    """

    job_title_normalized = normalize_skill(job_title)

    for role in candidate_roles:
        role_normalized = normalize_skill(role)

        if role_normalized in job_title_normalized:
            return 100.0

        if job_title_normalized in role_normalized:
            return 100.0

    # Basic keyword overlap
    job_words = set(job_title_normalized.split())

    for role in candidate_roles:
        role_words = set(normalize_skill(role).split())

        if job_words.intersection(role_words):
            return 70.0

    return 0.0


def calculate_match(
    candidate: dict[str, Any],
    job: dict[str, Any],
    requirements: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate the overall candidate-job match score.
    """

    skill_score, matched_skills, missing_skills = calculate_skill_score(
        candidate_skills=candidate["skills"],
        required_skills=requirements["required_skills"],
        preferred_skills=requirements["preferred_skills"],
    )

    experience_score = calculate_experience_score(
        candidate_experience=candidate["years_experience"],
        required_experience=requirements["min_experience"],
    )

    location_score = calculate_location_score(
        candidate_location=candidate.get("preferred_location"),
        job_location=job.get("location"),
        candidate_remote_preference=candidate.get(
            "remote_preference", False
        ),
        job_remote=job.get("remote", False),
    )

    role_score = calculate_role_score(
        candidate_roles=candidate["roles"],
        job_title=job["title"],
    )

    # Final weighted score
    match_score = (
        skill_score * 0.50
        + experience_score * 0.25
        + location_score * 0.15
        + role_score * 0.10
    )

    concerns = []

    if missing_skills:
        concerns.append(
            f"Missing required skills: {', '.join(missing_skills)}"
        )

    if requirements["min_experience"] is not None:
        if (
            float(candidate["years_experience"])
            < float(requirements["min_experience"])
        ):
            concerns.append(
                f"Job requires {requirements['min_experience']}+ years "
                f"of experience"
            )

    if location_score == 0:
        concerns.append("Location does not match candidate preference")

    return {
        "match_score": round(match_score, 2),
        "skill_score": skill_score,
        "experience_score": experience_score,
        "location_score": location_score,
        "role_score": role_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "concerns": concerns,
    }