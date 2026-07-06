from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import fitz

SKILL_KEYWORDS = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "React",
    "Next.js",
    "FastAPI",
    "Django",
    "Flask",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "SQLite",
    "MongoDB",
    "Redis",
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",
    "CI/CD",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "scikit-learn",
    "Data Analysis",
    "ETL",
    "Spark",
    "Airflow",
    "Linux",
    "Git",
    "REST API",
    "Microservices",
    "Leadership",
    "Communication",
    "Problem Solving",
]

CERTIFICATION_KEYWORDS = [
    "AWS Certified",
    "Azure",
    "GCP",
    "PMP",
    "Scrum",
    "Certified Kubernetes",
    "Salesforce",
]

EDUCATION_KEYWORDS = ["Bachelor", "Master", "B.Tech", "M.Tech", "B.E", "M.E", "PhD", "MBA"]


def extract_text_from_pdf(file_path: str | Path) -> str:
    text = []
    document = fitz.open(file_path)
    try:
        for page in document:
            text.append(page.get_text())
    finally:
        document.close()
    return "\n".join(text).strip()


def normalise_whitespace(value: str) -> str:
    return re.sub(r"[ \t]+", " ", value).strip()


def parse_job_description(title: str, description: str) -> dict[str, Any]:
    return {
        "title": title,
        "required_skills": find_keywords(description, SKILL_KEYWORDS),
        "years_experience_required": extract_years_required(description),
        "education": next((keyword for keyword in EDUCATION_KEYWORDS if re.search(keyword, description, re.I)), ""),
        "certifications": find_keywords(description, CERTIFICATION_KEYWORDS),
        "responsibilities": extract_bullets(description)[:8],
        "raw_jd": normalise_whitespace(description),
    }


def parse_resume_text(text: str, file_name: str) -> dict[str, Any]:
    cleaned = text.replace("\x00", " ")
    lines = [normalise_whitespace(line) for line in cleaned.splitlines() if normalise_whitespace(line)]
    top_chunk = "\n".join(lines[:20])
    summary = "\n".join(lines[:12])

    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", cleaned)
    phone_match = re.search(r"(?:\+\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}", cleaned)

    return {
        "name": extract_candidate_name(lines),
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "skills": sorted(set(find_keywords(cleaned, SKILL_KEYWORDS) + extract_skills_section(cleaned))),
        "education": extract_section(cleaned, ["education", "academic background"],
            ["experience", "skills", "projects", "certifications"]) or top_chunk,
        "work_experience": extract_section(cleaned, ["experience", "work experience", "employment history"],
            ["education", "skills", "projects", "certifications"]) or summary,
        "certifications": sorted(set(find_keywords(cleaned, CERTIFICATION_KEYWORDS))),
        "years_experience": estimate_years_experience(cleaned),
        "summary": summary,
        "raw_text": cleaned,
        "file_name": file_name,
    }


def extract_candidate_name(lines: list[str]) -> str:
    for line in lines[:8]:
        if "@" in line or any(char.isdigit() for char in line):
            continue
        if len(line.split()) >= 2 and len(line) <= 60:
            return line.title()
    return "Unknown Candidate"


def extract_section(text: str, headers: list[str], stop_headers: list[str]) -> str:
    header_pattern = "|".join(re.escape(header) for header in headers)
    stop_pattern = "|".join(re.escape(header) for header in stop_headers)
    match = re.search(
        rf"(?is)(?:{header_pattern})\s*:?\s*(.*?)(?:\n\s*(?:{stop_pattern})\s*:|\Z)",
        text,
    )
    if not match:
        return ""
    return normalise_whitespace(match.group(1))[:1200]


def extract_bullets(text: str) -> list[str]:
    bullets = re.findall(r"(?:^|\n)\s*(?:[-*•]|\d+\.)\s+(.*)", text)
    if bullets:
        return [normalise_whitespace(bullet) for bullet in bullets if bullet.strip()]
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [normalise_whitespace(sentence) for sentence in sentences if len(sentence.split()) > 5]


def find_keywords(text: str, keywords: list[str]) -> list[str]:
    found: list[str] = []
    for keyword in keywords:
        if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE):
            found.append(keyword)
    return found


def extract_skills_section(text: str) -> list[str]:
    section = extract_section(text, ["skills", "technical skills", "core competencies"],
        ["experience", "education", "projects", "certifications"])
    if not section:
        return []
    tokens = re.split(r"[,|/•\n]", section)
    return [normalise_whitespace(token) for token in tokens if 2 <= len(normalise_whitespace(token)) <= 40][:30]


def extract_years_required(text: str) -> dict[str, Any]:
    match = re.search(r"(\d+)(?:\s*-\s*(\d+))?\+?\s+years?", text, re.IGNORECASE)
    if not match:
        return {"minimum": 0.0, "label": "Not specified"}
    minimum = float(match.group(1))
    maximum = float(match.group(2)) if match.group(2) else minimum
    return {"minimum": minimum, "maximum": maximum, "label": match.group(0)}


def estimate_years_experience(text: str) -> float:
    explicit = re.findall(r"(\d+(?:\.\d+)?)\+?\s+years?", text, re.IGNORECASE)
    if explicit:
        return float(max(float(value) for value in explicit))

    ranges = re.findall(r"(20\d{2})\s*[-–]\s*(20\d{2}|present|current)", text, re.IGNORECASE)
    total = 0
    for start, end in ranges:
        end_year = 2026 if end.lower() in {"present", "current"} else int(end)
        start_year = int(start)
        if end_year >= start_year:
            total += end_year - start_year
    return float(total)
