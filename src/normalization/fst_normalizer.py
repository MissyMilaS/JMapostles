from typing import Dict, Iterable, List, Optional

from pyformlang.fst import FST


_TRANSDUCER_ALIASES = {
    "JAVASCRIPT": ("JS", "JavaScript"),
    "TYPESCRIPT": ("TS", "TypeScript"),
    "REACT": ("React.js", "ReactJS"),
    "NODE_JS": ("Node", "NodeJS", "Node.js", "Node JS"),
    "POSTGRESQL": ("Postgres",),
    "MYSQL": (),
    "MONGODB": (),
    "SQLITE": (),
    "SQL": (),
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
    "TERRAFORM": (),
    "JENKINS": (),
    "SPARK": (),
    "SNOWFLAKE": (),
    "AIRFLOW": (),
    "KAFKA": (),
}


def _input_symbol(qualification: str) -> str:
    return qualification.strip().casefold()


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
                transducer.add_transition(
                    parent_state, character, next_state, []
                )
        terminal_states.add(states_by_prefix[input_word])

    for state in terminal_states:
        transducer.add_transition(state, "epsilon", "qf", [canonical])

    return transducer


QUALIFICATION_TRANSDUCERS: Dict[str, FST] = {
    canonical: _build_transducer(canonical, aliases)
    for canonical, aliases in _TRANSDUCER_ALIASES.items()
}


def normalize_qualification(qualification: str) -> Optional[str]:
    if qualification is None:
        return None

    token = str(qualification).strip()
    if not token:
        return None

    input_word = _input_symbol(token)
    for transducer in QUALIFICATION_TRANSDUCERS.values():
        outputs = list(transducer.translate(input_word))
        if outputs:
            return outputs[0][0]

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
        if value not in seen:
            seen.add(value)
            normalized.append(value)
    return normalized
