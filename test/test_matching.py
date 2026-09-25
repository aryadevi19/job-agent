from app.services.matching_engine import calculate_match


candidate = {
    "years_experience": 1.5,
    "skills": [
        "Python",
        "FastAPI",
        "Docker",
        "Redis",
    ],
    "roles": [
        "Python Developer",
        "Backend Developer",
    ],
    "preferred_location": "Bangalore",
    "remote_preference": True,
}


job = {
    "title": "Python Developer",
    "location": "Bangalore",
    "remote": False,
}


requirements = {
    "required_skills": [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "MySQL",
    ],
    "preferred_skills": [
        "AWS",
        "Docker",
        "Redis",
        "CI/CD",
    ],
    "min_experience": 2,
}


result = calculate_match(
    candidate=candidate,
    job=job,
    requirements=requirements,
)

print(result)