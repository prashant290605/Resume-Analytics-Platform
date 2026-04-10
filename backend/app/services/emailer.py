from __future__ import annotations


def generate_interview_email(candidate_name: str, job_title: str, matched_skills: list[str]) -> str:
    skills_line = ""
    if matched_skills:
        skills_line = (
            "Your background stood out in particular because of your experience with "
            + ", ".join(matched_skills[:5])
            + ". "
        )

    return (
        f"Subject: Interview Invitation for {job_title}\n\n"
        f"Hi {candidate_name},\n\n"
        f"Thank you for applying for the {job_title} role. "
        f"{skills_line}"
        "We would love to move forward with an interview to learn more about your experience and discuss the role in more detail.\n\n"
        "Please reply with a few time slots that work for you over the next few days.\n\n"
        "Best,\nRecruiting Team"
    )
