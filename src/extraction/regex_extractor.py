import re
from typing import Dict, List, Any

PATTERNS = {
    "name": r'^\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
    "experience": r'(\d+\+?\s+years?\s+of\s+experience[^\.\n]*\.)',
    "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    "phone": r'\+?\d{1,3}?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}',
    "skills": r'\b(JS|JavaScript|Javascript|React\.js|React|ReactJS|NodeJS|Node\.js|Postgres|PostgreSQL|Git|REST APIs|Python|Pandas|pandas|NumPy|Scikit-learn|sklearn|scikit learn|TensorFlow|Tensor Flow|PyTorch|Py Torch|SQL|AWS|Docker|Kubernetes|Terraform|Jenkins|Spark|Snowflake|Airflow|Kafka)\b'
}

def extract_candidate_name(raw_text: str) -> str:
    match = re.search(PATTERNS["name"], raw_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    if not lines:
        return "Unknown Candidate"

    first_line = re.split(
        r"\b(?:PROFESSIONAL\s+)?WORK\s+EXPERIENCE\b",
        lines[0],
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0].strip()
    return first_line.title() if first_line else "Unknown Candidate"


def extract_contact_info(raw_text: str) -> Dict[str, str]:
    email_match = re.search(PATTERNS["email"], raw_text)
    phone_match = re.search(PATTERNS["phone"], raw_text)
    
    return {"email": email_match.group(0) if email_match else "Not provided","phone": phone_match.group(0) if phone_match else "Not provided"}


def extract_experience(raw_text: str) -> str:
    section_match = re.search(
        r"\b(?:PROFESSIONAL\s+)?WORK\s+EXPERIENCE\b\s*:?",
        raw_text,
        re.IGNORECASE,
    )
    if section_match:
        section_text = raw_text[section_match.end() :]
        section_text = re.split(
            r"\b(?:EDUCATION|TECHNICAL\s+SKILLS|SKILLS|PROJECTS|"
            r"CERTIFICATIONS|CERTIFICATES|LANGUAGES|PROFESSIONAL\s+SUMMARY|SUMMARY)"
            r"\s*:?\b",
            section_text,
            maxsplit=1,
            flags=re.IGNORECASE,
        )[0]
        section_text = re.sub(
            r"\s*([•▪●])\s*",
            lambda match: f"\n{match.group(1)} ",
            section_text,
        )
        section_lines = [line.rstrip() for line in section_text.splitlines()]

        while section_lines and not section_lines[-1].strip():
            section_lines.pop()

        while section_lines and re.fullmatch(
            r"[ \t]*[A-Z][A-Z0-9 &/()-]{1,40}:?[ \t]*", section_lines[-1]
        ):
            section_lines.pop()

        if section_lines and any(line.strip() for line in section_lines):
            return "\n".join(section_lines).strip()

    match = re.search(experience, raw_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Experience not specified."


def extract_raw_skills(raw_text: str) -> List[str]:
    matches = re.findall(PATTERNS["skills"], raw_text)
    
    seen = set()
    unique_skills = []
    for skill in matches:
        skill_clean = skill.strip()
        if skill_clean.lower() not in seen:
            seen.add(skill_clean.lower())
            unique_skills.append(skill_clean)
            
    return unique_skills


def stage_1_extract_resume_data(raw_text: str) -> Dict[str, Any]:
    return {"candidate_name": extract_candidate_name(raw_text),"contact_info": extract_contact_info(raw_text),"experience": extract_experience(raw_text),"extracted_skills": extract_raw_skills(raw_text)}