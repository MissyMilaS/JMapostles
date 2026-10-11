from typing import Iterable, List
from src.normalization.fst_normalizer import normalize_sequence

PROFILE_ORDERS = {
    "FULL_STACK": ("JAVASCRIPT","TYPESCRIPT","REACT","ANGULAR","VUE","NODE_JS","DJANGO","SPRING_BOOT","POSTGRESQL", "MYSQL","MONGODB","SQL","NOSQL","REST_API","GIT"),
    "ML_ENGINEER": ("PYTHON","PANDAS","NUMPY","SCIKIT_LEARN","TENSORFLOW","PYTORCH","POSTGRESQL","MYSQL","MONGODB","SQL","NOSQL","GIT"),
    "DEVOPS_ENGINEER": ("PYTHON", "DOCKER", "KUBERNETES", "AWS", "GIT"),
    "DATA_ENGINEER": ("PYTHON","PANDAS","SPARK","AIRFLOW","POSTGRESQL","MYSQL","MONGODB","SQL","NOSQL","GIT"),
}

def sort_canonical(qualifications: Iterable[str], profile: str = "FULL_STACK") -> List[str]:
    profile_name = profile.upper()
    if profile_name not in PROFILE_ORDERS:
        raise ValueError(f"Unsupported profile: {profile}")

    normalized = normalize_sequence(qualifications)
    rank = {token: index for index, token in enumerate(PROFILE_ORDERS[profile_name])}
    return sorted(normalized, key=lambda token: rank.get(token, len(rank)))