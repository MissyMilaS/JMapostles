from typing import Dict, Iterable, List

from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from src.normalization.fst_normalizer import QUALIFICATION_TRANSDUCERS


PROFILE_PATTERNS = {
    "FULL_STACK": ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
    "ML_ENGINEER": ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"],
    "DEVOPS_ENGINEER": ["PYTHON", "DOCKER", "KUBERNETES", "AWS", "GIT"],
    "DATA_ENGINEER": ["PYTHON", "SPARK", "AIRFLOW", "POSTGRESQL", "GIT"],
}
PROFILE_ALPHABET = frozenset(QUALIFICATION_TRANSDUCERS)
_REJECT_STATE = "q_reject"


def _build_profile_automaton(
    pattern: Iterable[str],
) -> DeterministicFiniteAutomaton:
    expected = list(pattern)
    automaton = DeterministicFiniteAutomaton()
    automaton.add_start_state("q0")

    for index, qualification in enumerate(expected):
        automaton.add_transition(f"q{index}", qualification, f"q{index + 1}")
        for other_symbol in PROFILE_ALPHABET - {qualification}:
            automaton.add_transition(f"q{index}", other_symbol, _REJECT_STATE)

    accepting_state = f"q{len(expected)}"
    automaton.add_final_state(accepting_state)
    for symbol in PROFILE_ALPHABET:
        automaton.add_transition(accepting_state, symbol, _REJECT_STATE)
        automaton.add_transition(_REJECT_STATE, symbol, _REJECT_STATE)

    return automaton


PROFILE_AUTOMATA: Dict[str, DeterministicFiniteAutomaton] = {
    profile: _build_profile_automaton(pattern)
    for profile, pattern in PROFILE_PATTERNS.items()
}


def normalize_profile_name(profile: str) -> str:
    if profile is None:
        raise ValueError("A professional profile must be specified.")

    cleaned = "".join(character for character in profile.casefold() if character.isalnum())
    aliases = {
        "fullstack": "FULL_STACK",
        "fullstackdeveloper": "FULL_STACK",
        "mlengineer": "ML_ENGINEER",
        "machinelearningengineer": "ML_ENGINEER",
        "devopsengineer": "DEVOPS_ENGINEER",
        "dataengineer": "DATA_ENGINEER",
    }
    try:
        return aliases[cleaned]
    except KeyError as error:
        raise ValueError(f"Unsupported professional profile: {profile}") from error


def evaluate_profile(
    qualifications: Iterable[str], profile: str
) -> str:
    profile_name = normalize_profile_name(profile)
    return (
        "ACCEPTED"
        if PROFILE_AUTOMATA[profile_name].accepts(list(qualifications))
        else "REJECTED"
    )


def evaluate_full_stack(qualifications: Iterable[str]) -> str:
    return evaluate_profile(qualifications, "FULL_STACK")


def evaluate_ml_engineer(qualifications: Iterable[str]) -> str:
    return evaluate_profile(qualifications, "ML_ENGINEER")


def evaluate_devops_engineer(qualifications: Iterable[str]) -> str:
    return evaluate_profile(qualifications, "DEVOPS_ENGINEER")


def evaluate_data_engineer(qualifications: Iterable[str]) -> str:
    return evaluate_profile(qualifications, "DATA_ENGINEER")


def evaluate_all_profiles(qualifications: Iterable[str]) -> Dict[str, str]:
    qualification_sequence: List[str] = list(qualifications)
    return {
        profile: evaluate_profile(qualification_sequence, profile)
        for profile in PROFILE_PATTERNS
    }
