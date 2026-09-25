import json

from google import genai

from app.core.config import settings
from app.schemas.job_requirement import JobRequirementCreate


client = genai.Client(
    api_key=settings.google_api_key
)


SYSTEM_PROMPT = """
You are a job requirement extraction system.

Your task is to extract structured requirements from a job description.

Rules:
- Extract only information explicitly stated or strongly implied by the job description.
- Do not invent skills or requirements.
- Separate required skills from preferred/nice-to-have skills.
- If experience is not specified, return null.
- If education is not specified, return an empty list.
- If required keywords are not clear, return an empty list.
- Extract important responsibilities.
- Normalize technology names where appropriate.
  Example: "Postgres" -> "PostgreSQL".
"""


def extract_job_requirements(
    title: str,
    description: str,
) -> JobRequirementCreate:

    prompt = f"""
{SYSTEM_PROMPT}

Job title:
{title}

Job description:
{description}

Return ONLY valid JSON with this structure:

{{
    "required_skills": [],
    "preferred_skills": [],
    "min_experience": null,
    "education": [],
    "required_keywords": [],
    "responsibilities": []
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
        },
    )

    data = json.loads(response.text)

    return JobRequirementCreate.model_validate(data)