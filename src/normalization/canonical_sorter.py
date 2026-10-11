from typing import Iterable, List, Optional

from src.normalization.fst_normalizer import normalize_sequence


_PROFILE_ORDER = {
    "FULL_STACK": [
        "JAVASCRIPT",
        "REACT",
        "NODE_JS",
        "POSTGRESQL",
        "GIT",
    ],
    "ML_ENGINEER": [
        "PYTHON",
        "PANDAS",
        "TENSORFLOW",
        "POSTGRESQL",
        "GIT",
    ],
    "DEVOPS_ENGINEER": [
        "PYTHON",
        "DOCKER",
        "KUBERNETES",
        "AWS",
        "GIT",
    ],
    "DATA_ENGINEER": [
        "PYTHON",
        "SPARK",
        "AIRFLOW",
        "POSTGRESQL",
        "GIT",
    ],
}


def _normalize_profile_name(profile: Optional[str]) -> str:
    if profile is None:
        return "FULL_STACK"

    cleaned = profile.strip().upper().replace("-", "_").replace(" ", "_")
    if cleaned in _PROFILE_ORDER:
        return cleaned
    for key in _PROFILE_ORDER:
        if key.replace("_", "") == cleaned.replace("_", ""):
            return key
    return "FULL_STACK"


def sort_canonical(qualifications: Iterable[str], profile: Optional[str] = "FULL_STACK") -> List[str]:
    normalized = normalize_sequence(qualifications)
    if not normalized:
        return []

    profile_name = _normalize_profile_name(profile)
    order = {value: idx for idx, value in enumerate(_PROFILE_ORDER.get(profile_name, normalized))}

    return sorted(normalized, key=lambda item: order.get(item, len(order)))
