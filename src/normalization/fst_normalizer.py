import re
from typing import Dict, Iterable, List, Optional

from pyformlang.fst import FST


_TRANSDUCER_ALIASES = {
    "JAVASCRIPT": ("JS", "JavaScript"),
    "TYPESCRIPT": ("TS", "TypeScript"),
    "REACT": ("React.js", "ReactJS"),
    "ANGULAR": ("Angular.js",),
    "VUE": ("Vue.js",),
    "NODE_JS": ("Node", "NodeJS", "Node.js", "Node JS"),
    "DJANGO": (),
    "SPRING_BOOT": ("Spring Boot", "SpringBoot"),
    "POSTGRESQL": ("Postgres",),
    "MYSQL": (),
    "MONGODB": (),
    "SQL": (),
    "SQLITE": (),
    "NOSQL": ("No SQL",),
    "REST_API": ("REST API", "REST APIs", "RESTful API", "RESTful APIs"),
    "PYTHON": (),
    "PANDAS": (),
    "NUMPY": (),
    "SCIKIT_LEARN": ("sklearn", "scikit-learn", "scikit learn"),
    "TENSORFLOW": ("Tensor Flow",),
    "PYTORCH": ("Py Torch",),
    "GIT": (),
    "GITHUB": (),
    "GITHUB_ACTIONS": ("GitHub Actions",),
    "DOCKER": (),
    "KUBERNETES": (),
    "AWS": (),
    "AZURE": (),
    "GCP": (),
    "TERRAFORM": (),
    "JENKINS": (),
    "SPARK": (),
    "SNOWFLAKE": (),
    "AIRFLOW": (),
    "KAFKA": (),
}


def _input_symbol(qualification: str) -> str:
    return re.sub(r"\s+", " ", qualification.strip().casefold())


def _build_transducer(canonical: str, aliases: Iterable[str]) -> FST:
    transducer = FST()
    transducer.add_start_state("q0")
    transducer.add_final_state("qf")

    states_by_prefix = {"": "q0"}
    terminal_states = set()
    next_state_number = 1
    input_words = {_input_symbol(canonical), *(_input_symbol(alias) for alias in aliases)}

    for input_word in input_words:
        for index, character in enumerate(input_word):
            prefix = input_word[: index + 1]
            if prefix not in states_by_prefix:
                next_state = f"q{next_state_number}"
                next_state_number += 1
                parent_state = states_by_prefix[input_word[:index]]
                states_by_prefix[prefix] = next_state
                transducer.add_transition(parent_state, character, next_state, [])
        terminal_states.add(states_by_prefix[input_word])

    for state in terminal_states:
        transducer.add_transition(state, "epsilon", "qf", [canonical])

    return transducer


QUALIFICATION_TRANSDUCERS: Dict[str, FST] = {
    canonical: _build_transducer(canonical, aliases)
    for canonical, aliases in _TRANSDUCER_ALIASES.items()
}


def normalize_qualification(qualification: Optional[str]) -> Optional[str]:
    if qualification is None:
        return None

    input_word = _input_symbol(str(qualification))
    if not input_word:
        return None

    for transducer in QUALIFICATION_TRANSDUCERS.values():
        outputs = list(transducer.translate(input_word))
        if outputs:
            return outputs[0][0]

    return "UNKNOWN"


def normalize_sequence(qualifications: Optional[Iterable[str]]) -> List[str]:
    if qualifications is None:
        return []

    normalized: List[str] = []
    seen = set()
    for qualification in qualifications:
        value = normalize_qualification(qualification)
        if value in (None, "UNKNOWN"):
            continue
        if value not in seen:
            seen.add(value)
            normalized.append(value)
    return normalized
