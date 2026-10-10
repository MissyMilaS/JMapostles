import re
from typing import Dict, List, Any

experience = r'(\d+\+?\s+years?\s+of\s+experience[^\.\n]*\.)'
skills = r'\b(JS|JavaScript|TypeScript|React\.js|React|Redux|NodeJS|Express\.js|Postgres|PostgreSQL|Git|REST APIs|Python|Pandas|NumPy|Scikit-learn|TensorFlow|SQL|AWS|Docker|Kubernetes|Terraform|Jenkins|Spark|Snowflake|Airflow|Kafka)\b'
phone = r'\+?\d{1,3}?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

def extract_name(raw_text: str) -> str:
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    return lines[0].title() if lines else "Unknown Candidate"


def extract_experience(raw_text: str) -> str:
    match = re.search(experience, raw_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Experience not specified."


def extract_raw_skills(raw_text: str) -> List[str]:
    """Extrae todas las coincidencias de habilidades técnicas sin duplicados."""
    matches = re.findall(skills, raw_text, re.IGNORECASE)
    
    # Preserva el orden original de aparición eliminando duplicados
    seen = set()
    unique_skills = []
    for skill in matches:
        skill_upper = skill.strip()
        if skill_upper.lower() not in seen:
            seen.add(skill_upper.lower())
            unique_skills.append(skill_upper)
            
    return unique_skills


def process_resume_to_short_cv(raw_text: str) -> Dict[str, Any]:
    name = extract_name(raw_text)
    experience = extract_experience(raw_text)
    raw_skills = extract_raw_skills(raw_text)
    
    # Construir el formato textual del "CV Corto"
    skills_str = ", ".join(raw_skills)
    short_cv_text = f"{name} | {experience} | Technical Skills: {skills_str}."
    
    return {
        "candidate_name": name,
        "experience": experience,
        "raw_skills": raw_skills,
        "short_cv_text": short_cv_text
    }