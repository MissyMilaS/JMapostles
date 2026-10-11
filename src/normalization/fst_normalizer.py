import re
from typing import Iterable, List

from pyformlang.fst import FST


ALIASES = {
    "JAVASCRIPT": ("javascript", "js"),
    "TYPESCRIPT": ("typescript", "ts"),
    "REACT": ("react", "react.js", "reactjs"),
    "ANGULAR": ("angular", "angular.js"),
    "VUE": ("vue", "vue.js"),
    "NODE_JS": ("nodejs", "node.js", "node js"),
    "DJANGO": ("django",),
    "SPRING_BOOT": ("spring boot", "springboot"),
    "POSTGRESQL": ("postgres", "postgresql"),
    "MYSQL": ("mysql",),
    "MONGODB": ("mongodb",),
    "SQL": ("sql",),
    "NOSQL": ("nosql", "no sql"),
    "REST_API": ("rest api", "rest apis", "restful api", "restful apis"),
    "GIT": ("git", "github"),
    "PYTHON": ("python",),
    "PANDAS": ("pandas",),
    "NUMPY": ("numpy",),
    "SCIKIT_LEARN": ("scikit-learn", "scikit learn", "sklearn"),
    "TENSORFLOW": ("tensorflow", "tensor flow"),
    "PYTORCH": ("pytorch", "py torch"),
    "AWS": ("aws",),
    "DOCKER": ("docker",),
    "KUBERNETES": ("kubernetes",),
    "TERRAFORM": ("terraform",),
    "JENKINS": ("jenkins",),
    "SPARK": ("spark",),
    "SNOWFLAKE": ("snowflake",),
    "AIRFLOW": ("airflow",),
    "KAFKA": ("kafka",),
}


def _build_transducer() -> FST:
    transducer = FST()
    transducer.add_start_state(0)
    next_state = 1

    for canonical_name, aliases in ALIASES.items():
        for alias in (*aliases, canonical_name.casefold()):
            normalized_alias = re.sub(r"\s+", " ", alias.casefold().strip())
            state = 0

            for index, character in enumerate(normalized_alias):
                destination = next_state
                next_state += 1
                output = [canonical_name] if index == len(normalized_alias) - 1 else []
                transducer.add_transition(state, character, destination, output)
                state = destination

            transducer.add_final_state(state)

    return transducer


_QUALIFICATION_TRANSDUCER = _build_transducer()


def normalize_qualification(qualification: str) -> str:
    normalized_input = re.sub(r"\s+", " ", qualification.casefold().strip())
    if not normalized_input:
        return "UNKNOWN"

    translations = _QUALIFICATION_TRANSDUCER.translate(normalized_input)
    return next(iter(translations), ["UNKNOWN"])[0]


def normalize_sequence(qualifications: Iterable[str]) -> List[str]:
    normalized = []
    seen = set()

    for qualification in qualifications:
        canonical_name = normalize_qualification(qualification)
        if canonical_name != "UNKNOWN" and canonical_name not in seen:
            seen.add(canonical_name)
            normalized.append(canonical_name)

    return normalized