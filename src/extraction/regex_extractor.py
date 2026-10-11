import re
from typing import Any, Dict, List, Pattern


PATTERNS = {
    "name": re.compile(
        r"^\s*([A-Z][A-Za-z0-9'’-]*(?:[ \t]+[A-Z][A-Za-z0-9'’-]*)+)",
        re.MULTILINE,
    ),
    "email": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
    "phone": re.compile(r"(?<!\w)\+?\d{1,3}(?:[\s().-]*\d){7,14}(?!\w)"),
    "url": re.compile(
        r"(?i)(?<![\w@])(?:https?://|www\.)[^\s|,<>]+|"
        r"(?<![\w@])(?:github\.com/[A-Za-z0-9_.%-]+|"
        r"linkedin\.com/(?:in|company)/[A-Za-z0-9_.%-]+)"
    ),
    "programming_languages": re.compile(
        r"\b(?:JavaScript|Javascript|(?<![\w.])JS(?![\w.])|TypeScript|TS|Python|Java|"
        r"C\+\+|C#|Go|Golang|Ruby|PHP|Kotlin|Swift|Rust|Scala|R)\b",
        re.IGNORECASE,
    ),
    "frameworks": re.compile(
        r"\b(?:Spring\s+Boot|React\.js|ReactJS|React|Angular\.js|Angular|"
        r"Vue\.js|Vue|Node\.js|NodeJS|Express\.js|Express|Django|Flask|"
        r"FastAPI|Laravel|Rails|ASP\.NET|\.NET)\b",
        re.IGNORECASE,
    ),
    "databases": re.compile(
        r"\b(?:Microsoft SQL Server|PostgreSQL|Postgres|MySQL|MongoDB|NoSQL|SQL|"
        r"SQLite|Redis|Oracle|Cassandra|DynamoDB|MariaDB)\b",
        re.IGNORECASE,
    ),
    "ml_libraries": re.compile(
        r"\b(?:Scikit-learn|scikit\s+learn|sklearn|TensorFlow|Tensor\s+Flow|"
        r"PyTorch|Py\s+Torch|Pandas|NumPy|Keras|OpenCV|Hugging\s*Face|XGBoost|SciPy)\b",
        re.IGNORECASE,
    ),
    "tools": re.compile(
        r"\b(?:RESTful\s+APIs?|REST\s+APIs?|GitHub|GitLab|Bitbucket|Git|Docker|"
        r"Kubernetes|Terraform|Jenkins|AWS|Azure|GCP|Spark|Snowflake|Airflow|Kafka)\b",
        re.IGNORECASE,
    ),
    "qualifications": re.compile(
        r"\b(?:Microsoft SQL Server|Spring\s+Boot|React\.js|ReactJS|Angular\.js|Vue\.js|"
        r"Node\.js|Express\.js|ASP\.NET|PostgreSQL|Scikit-learn|scikit\s+learn|"
        r"Tensor\s+Flow|Py\s+Torch|Hugging\s*Face|RESTful\s+APIs?|REST\s+APIs?|"
        r"JavaScript|Javascript|JS|TypeScript|TS|Python|Java|C\+\+|C#|Go|Golang|"
        r"Ruby|PHP|Kotlin|Swift|Rust|Scala|R|React|Angular|Vue|NodeJS|Node|Express|"
        r"Django|Flask|FastAPI|Laravel|Rails|\.NET|Postgres|MySQL|MongoDB|NoSQL|SQL|"
        r"SQLite|Redis|Oracle|Cassandra|DynamoDB|MariaDB|sklearn|TensorFlow|PyTorch|"
        r"Pandas|NumPy|Keras|OpenCV|XGBoost|SciPy|GitHub|GitLab|Bitbucket|Git|Docker|"
        r"Kubernetes|Terraform|Jenkins|AWS|Azure|GCP|Spark|Snowflake|Airflow|Kafka)\b",
        re.IGNORECASE,
    ),
    "degree": re.compile(
        r"\b(?:B\.S\.|B\.A\.|M\.S\.|M\.A\.|Ph\.D\.|Doctorate|Doctoral|"
        r"Master(?:'s)?|Bachelor(?:'s)?|Associate(?:'s)?|Licenciatura|Tecn[oó]logo)"
        r"(?:[ \t]+(?:degree[ \t]+)?(?:of|in|de|en)[ \t]+"
        r"[A-Za-z][A-Za-z&./'-]*(?:[ \t]+[A-Za-z][A-Za-z&./'-]*){0,5})?",
        re.IGNORECASE,
    ),
    "experience_years": re.compile(
        r"\b(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|"
        r"eleven|twelve)\+?\s+years?\s+(?:of\s+)?experience\b",
        re.IGNORECASE,
    ),
}

_NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}
_SECTION_HEADING = re.compile(
    r"\b(?:WORK\s+EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|EXPERIENCE|"
    r"EDUCATION|ACADEMIC\s+BACKGROUND|TECHNICAL\s+SKILLS|SKILLS|"
    r"PROJECTS|CERTIFICATIONS|CERTIFICATES|LANGUAGES|"
    r"PROFESSIONAL\s+SUMMARY|SUMMARY)\b\s*:?",
    re.IGNORECASE,
)
_EXPERIENCE_HEADING = re.compile(
    r"\b(?:WORK\s+EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|EXPERIENCE)\b\s*:?",
    re.IGNORECASE,
)
_EDUCATION_HEADING = re.compile(
    r"\b(?:EDUCATION|ACADEMIC\s+BACKGROUND)\b\s*:?",
    re.IGNORECASE,
)


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

    section = re.sub(
        r"(?<!\n)[ \t]*([•▪●◦])[ \t]*",
        lambda bullet: f"\n{bullet.group(1)} ",
        section,
    )
    return section.strip(" \t\r\n:-")


def extract_candidate_name(raw_text: str) -> str:
    for line in raw_text.splitlines() or [raw_text]:
        candidate = line.strip()
        if not candidate:
            continue
        heading = _SECTION_HEADING.search(candidate)
        if heading:
            candidate = candidate[: heading.start()].strip(" \t:-|")
        candidate = re.split(r"[\t|]", candidate, maxsplit=1)[0].strip()
        if not candidate:
            continue
        match = PATTERNS["name"].match(candidate)
        if match:
            return match.group(1).strip()
        if "@" not in candidate and not re.search(r"\d{5,}", candidate):
            return candidate
    return "Unknown Candidate"


def extract_contact_info(raw_text: str) -> Dict[str, List[str]]:
    return {
        "emails": _unique_matches(PATTERNS["email"], raw_text),
        "phones": _unique_matches(PATTERNS["phone"], raw_text),
        "urls": _unique_matches(PATTERNS["url"], raw_text),
    }


def extract_programming_languages(raw_text: str) -> List[str]:
    return _unique_matches(PATTERNS["programming_languages"], raw_text)


def extract_frameworks(raw_text: str) -> List[str]:
    return _unique_matches(PATTERNS["frameworks"], raw_text)


def extract_databases(raw_text: str) -> List[str]:
    return _unique_matches(PATTERNS["databases"], raw_text)


def extract_ml_libraries(raw_text: str) -> List[str]:
    return _unique_matches(PATTERNS["ml_libraries"], raw_text)


def extract_tools(raw_text: str) -> List[str]:
    return _unique_matches(PATTERNS["tools"], raw_text)


def extract_raw_skills(raw_text: str) -> List[str]:
    return _unique_matches(PATTERNS["qualifications"], raw_text)


def extract_all_qualifications(raw_text: str) -> List[str]:
    return extract_raw_skills(raw_text)


def extract_experience_and_education(raw_text: str) -> Dict[str, Any]:
    degree_match = PATTERNS["degree"].search(raw_text)
    years_match = PATTERNS["experience_years"].search(raw_text)
    years = 0
    if years_match:
        value = years_match.group(1).casefold()
        years = int(value) if value.isdigit() else _NUMBER_WORDS[value]
    return {
        "degree": degree_match.group(0).strip(" \t.,;") if degree_match else None,
        "years_experience": years,
    }


def extract_experience(raw_text: str) -> str:
    section = _extract_section(raw_text, _EXPERIENCE_HEADING)
    if section:
        return section

    years_match = PATTERNS["experience_years"].search(raw_text)
    if years_match:
        sentence_start = raw_text.rfind(".", 0, years_match.start()) + 1
        sentence_end = raw_text.find(".", years_match.end())
        if sentence_end < 0:
            sentence_end = len(raw_text)
        sentence = raw_text[sentence_start:sentence_end].strip()
        if sentence:
            return sentence
    return "Experience not specified."


def stage_1_extract_resume_data(raw_text: str) -> Dict[str, Any]:
    education_section = _extract_section(raw_text, _EDUCATION_HEADING)
    experience_details = extract_experience_and_education(raw_text)
    skills = extract_all_qualifications(raw_text)
    return {
        "candidate_name": extract_candidate_name(raw_text),
        "contact_info": extract_contact_info(raw_text),
        "education": {
            "degree": experience_details["degree"],
            "section": education_section,
        },
        "experience": extract_experience(raw_text),
        "years_experience": experience_details["years_experience"],
        "programming_languages": extract_programming_languages(raw_text),
        "frameworks": extract_frameworks(raw_text),
        "databases": extract_databases(raw_text),
        "ml_libraries": extract_ml_libraries(raw_text),
        "tools": extract_tools(raw_text),
        "extracted_skills": skills,
        "raw_skills": skills,
    }


def process_resume_to_short_cv(raw_text: str) -> Dict[str, Any]:
    """Return the extracted resume data with a concise readable summary."""
    result = stage_1_extract_resume_data(raw_text)
    contact = result["contact_info"]
    skills = ", ".join(result["extracted_skills"]) or "None identified"
    result["short_cv_text"] = (
        f"{result['candidate_name']} | {result['experience']} | "
        f"Technical Skills: {skills}."
    )
    result["contact_summary"] = ", ".join(
        contact[key][0] for key in ("emails", "phones") if contact[key]
    ) or "Contact information not provided."
    return result
