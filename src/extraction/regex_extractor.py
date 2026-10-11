import re
from typing import Any, Dict, List, Pattern


PATTERNS = {
    "name": re.compile(r"^\s*([A-Z][\w'-]*(?:\s+[A-Z][\w'-]*)+)", re.MULTILINE),
    "email": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
    "phone": re.compile(r"(?<!\w)\+?\d{1,3}(?:[\s().-]*\d){7,14}(?!\w)"),
    "url": re.compile( r"(?i)(?<![\w@])(?:https?://|www\.)[^\s|,<>]+|" r"(?<![\w@])(?:github\.com/[A-Za-z0-9_.%-]+|" r"linkedin\.com/(?:in|company)/[A-Za-z0-9_.%-]+)"),
    "programming_languages": re.compile(r"\b(?:JavaScript|Javascript|(?<![\w.])JS(?![\w.])|TypeScript|TS|Python|Java|C\+\+|C#|"r"Go|Golang|Ruby|PHP|Kotlin|Swift|Rust|Scala|R)\b",re.IGNORECASE),
    "frameworks": re.compile( r"\b(?:Spring\s+Boot|React\.js|ReactJS|React|Angular\.js|Angular|" r"Vue\.js|Vue|Node\.js|NodeJS|Express\.js|Express|Django|Flask|" r"FastAPI|Laravel|Rails|ASP\.NET|\.NET)\b", re.IGNORECASE),
    "databases": re.compile( r"\b(?:PostgreSQL|Postgres|MySQL|MongoDB|NoSQL|SQL|SQLite|" r"Redis|Oracle|Cassandra|DynamoDB|MariaDB|Microsoft SQL Server)\b", re.IGNORECASE),
    "ml_libraries": re.compile(r"\b(?:Scikit-learn|scikit\s+learn|sklearn|TensorFlow|Tensor\s+Flow|"r"PyTorch|Py\s+Torch|Pandas|NumPy|Keras|OpenCV|Hugging\s*Face|"r"XGBoost|SciPy)\b", re.IGNORECASE),
    "tools": re.compile(r"\b(?:GitHub|GitLab|Bitbucket|Git|Docker|Kubernetes|Terraform|"r"Jenkins|AWS|Azure|GCP|Spark|Snowflake|Airflow|Kafka|"r"RESTful\s+APIs?|REST\s+APIs?)\b", re.IGNORECASE),
    "qualifications": re.compile(
        r"\b(?:JavaScript|Javascript|JS|TypeScript|TS|Python|Java|C\+\+|C#|"
        r"Go|Golang|Ruby|PHP|Kotlin|Swift|Rust|Scala|R|"
        r"Spring\s+Boot|React\.js|ReactJS|React|Angular\.js|Angular|"
        r"Vue\.js|Vue|Node\.js|NodeJS|Express\.js|Express|Django|Flask|"
        r"FastAPI|Laravel|Rails|ASP\.NET|\.NET|"
        r"PostgreSQL|Postgres|MySQL|MongoDB|NoSQL|SQL|SQLite|Redis|Oracle|"
        r"Cassandra|DynamoDB|MariaDB|Microsoft SQL Server|"
        r"RESTful\s+APIs?|REST\s+APIs?|"
        r"Scikit-learn|scikit\s+learn|sklearn|TensorFlow|Tensor\s+Flow|"
        r"PyTorch|Py\s+Torch|Pandas|NumPy|Keras|OpenCV|Hugging\s*Face|"
        r"XGBoost|SciPy|GitHub|GitLab|Bitbucket|Git|Docker|Kubernetes|"
        r"Terraform|Jenkins|AWS|Azure|GCP|Spark|Snowflake|Airflow|Kafka)\b",
        re.IGNORECASE,
    ),
    "degree": re.compile(r"\b(?:B\.S\.|B\.A\.|M\.S\.|M\.A\.|Ph\.D\.|Doctorate|Doctoral|"r"Master(?:'s)?|Bachelor(?:'s)?|Associate(?:'s)?|Licenciatura|"r"Tecn[oó]logo)"r"(?:[ \t]+(?:degree[ \t]+)?(?:of|in|de|en)[ \t]+"r"[A-Za-z][A-Za-z&./'-]*(?:[ \t]+[A-Za-z][A-Za-z&./'-]*){0,5})?", re.IGNORECASE,),
    "experience_years": re.compile( r"\b(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|" r"eleven|twelve)\+?\s+years?\s+(?:of\s+)?experience\b", re.IGNORECASE),
}

_NUMBER_WORDS = {"one": 1,"two": 2,"three": 3,"four": 4,"five": 5,"six": 6,"seven": 7,"eight": 8,"nine": 9,"ten": 10,"eleven": 11,"twelve": 12}
_SECTION_HEADING = re.compile(r"\b(?:WORK\s+EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|EXPERIENCE|"r"EDUCATION|ACADEMIC\s+BACKGROUND|TECHNICAL\s+SKILLS|SKILLS|"r"PROJECTS|CERTIFICATIONS|CERTIFICATES|LANGUAGES|"r"PROFESSIONAL\s+SUMMARY|SUMMARY)\b\s*:?",re.IGNORECASE)
_EXPERIENCE_HEADING = re.compile( r"\b(?:WORK\s+EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|EXPERIENCE)\b\s*:?", re.IGNORECASE)
_EDUCATION_HEADING = re.compile(r"\b(?:EDUCATION|ACADEMIC\s+BACKGROUND)\b\s*:?", re.IGNORECASE)


def _unique_matches(pattern: Pattern[str], raw_text: str) -> List[str]:
    matches = []
    seen = set()
    for match in pattern.finditer(raw_text):
        value = match.group(0).strip().rstrip(".,;)")
        key = value.casefold()
        if value and key not in seen:
            seen.add(key)
            matches.append(value)
    return matches


def _extract_section(raw_text: str, heading: Pattern[str]) -> str:
    match = heading.search(raw_text)
    if not match:
        return ""

    section = raw_text[match.end() :]
    next_heading = _SECTION_HEADING.search(section)
    if next_heading:
        section = section[: next_heading.start()]

    section = re.sub(r"(?m)^[ \t]*([•▪●◦*-])[ \t]*",lambda bullet: f"\n{bullet.group(1)} ",section)
    section = re.sub( r"[ \t]*([•▪●◦])[ \t]*",lambda bullet: f"\n{bullet.group(1)} ", section)
    return section.strip(" \t\r\n:-")


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


def stage_1_extract_resume_data(raw_text: str) -> Dict[str, Any]:
    education = _extract_section(raw_text, _EDUCATION_HEADING)
    experience_details = extract_experience_and_education(raw_text)
    return {"candidate_name": extract_candidate_name(raw_text),"contact_info": extract_contact_info(raw_text),"education": {
            "degree": experience_details["degree"],"section": education},
        "experience": extract_experience(raw_text),
        "years_experience": experience_details["years_experience"],
        "programming_languages": extract_programming_languages(raw_text),
        "frameworks": extract_frameworks(raw_text),
        "databases": extract_databases(raw_text),
        "ml_libraries": extract_ml_libraries(raw_text),
        "tools": extract_tools(raw_text),
        "extracted_skills": extract_all_qualifications(raw_text),
    }


def process_resume_to_short_cv(raw_text: str) -> Dict[str, Any]:
    result = stage_1_extract_resume_data(raw_text)
    contact = result["contact_info"]
    skills = ", ".join(result["extracted_skills"]) or "None identified"
    experience = result["experience"]
    result["short_cv_text"] = (
        f"{result['candidate_name']} | {experience} | Technical Skills: {skills}."
    )
    result["contact_summary"] = ", ".join(
        contact[key][0] for key in ("emails", "phones") if contact[key]
    ) or "Contact information not provided."
    return result
