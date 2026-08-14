"""
Job Description Parser - Validates and processes job descriptions.
"""


def validate_jd(text: str) -> dict:
    """
    Validate a job description and return quality metrics.
    """
    issues = []
    word_count = len(text.split()) if text else 0

    if word_count < 10:
        issues.append("Job description is extremely short.")
    elif word_count < 30:
        issues.append("Job description is very short. More detail will improve analysis accuracy.")

    # Check for common JD elements
    common_elements = [
        "requirement", "responsibility", "qualification", "skill",
        "experience", "education", "role", "position", "job",
        "team", "company", "description", "looking", "candidate"
    ]
    text_lower = text.lower()
    found_elements = [e for e in common_elements if e in text_lower]

    if len(found_elements) < 2:
        issues.append(
            "Job description may not contain standard elements "
            "(requirements, responsibilities, qualifications, skills)."
        )

    return {
        "word_count": word_count,
        "issues": issues,
        "elements_found": found_elements,
        "is_valid": word_count >= 10,
    }
