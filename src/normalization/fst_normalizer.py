import re
from typing import Iterable, List, Optional


def _key(qualification: str) -> str:
    if qualification is None:
        return ""
    return re.sub(r"[^a-z0-9]", "", str(qualification).strip().lower())


def normalize_qualification(qualification: str) -> Optional[str]:
    if qualification is None:
        return None

    token = str(qualification).strip()
    if not token:
        return None

    mapping = {
        "js": "JAVASCRIPT",
        "javascript": "JAVASCRIPT",
        "typescript": "TYPESCRIPT",
        "ts": "TYPESCRIPT",
        "react": "REACT",
        "reactjs": "REACT",
        "nodejs": "NODE_JS",
        "node": "NODE_JS",
        "postgres": "POSTGRESQL",
        "postgresql": "POSTGRESQL",
        "mysql": "MYSQL",
        "mongodb": "MONGODB",
        "sqlite": "SQLITE",
        "sql": "SQL",
        "python": "PYTHON",
        "pandas": "PANDAS",
        "numpy": "NUMPY",
        "sklearn": "SCIKIT_LEARN",
        "scikitlearn": "SCIKIT_LEARN",
        "tensorflow": "TENSORFLOW",
        "pytorch": "PYTORCH",
        "git": "GIT",
        "github": "GIT",
        "githubactions": "GITHUB_ACTIONS",
        "docker": "DOCKER",
        "kubernetes": "KUBERNETES",
        "aws": "AWS",
        "terraform": "TERRAFORM",
        "jenkins": "JENKINS",
        "spark": "SPARK",
        "snowflake": "SNOWFLAKE",
        "airflow": "AIRFLOW",
        "kafka": "KAFKA",
    }

    key = _key(token)
    if key in mapping:
        return mapping[key]

    return "UNKNOWN"


def normalize_sequence(qualifications: Iterable[str]) -> List[str]:
    if qualifications is None:
        return []

    normalized: List[str] = []
    seen = set()
    for qualification in qualifications:
        value = normalize_qualification(qualification)
        if value in (None, "UNKNOWN"):
            continue
        if value.lower() not in seen:
            seen.add(value.lower())
            normalized.append(value)
    return normalized
