from typing import Iterable, Sequence, Set, Tuple

from pyformlang.finite_automaton import DeterministicFiniteAutomaton


ACCEPTED = "ACCEPTED"
REJECTED = "REJECTED"

_DATABASES = {"POSTGRESQL", "MYSQL", "MONGODB", "SQL", "NOSQL"}
_FULL_STACK_STAGES: Tuple[Set[str], ...] = (
    {"JAVASCRIPT", "TYPESCRIPT"},
    {"REACT", "ANGULAR", "VUE"},
    {"NODE_JS", "DJANGO", "SPRING_BOOT"},
    _DATABASES,
    {"GIT"},
)
_PROFILE_STAGES = {
    "FULL_STACK": _FULL_STACK_STAGES,
    "ML_ENGINEER": (
        {"PYTHON"},
        {"PANDAS", "NUMPY"},
        {"SCIKIT_LEARN", "TENSORFLOW", "PYTORCH"},
        _DATABASES,
        {"GIT"},
    ),
    "DEVOPS_ENGINEER": (
        {"PYTHON"},
        {"DOCKER"},
        {"KUBERNETES"},
        {"AWS"},
        {"GIT"},
    ),
    "DATA_ENGINEER": (
        {"PYTHON"},
        {"PANDAS", "NUMPY"},
        {"SPARK"},
        {"AIRFLOW"},
        _DATABASES,
        {"GIT"},
    ),
}
_KNOWN_TOKENS = set().union(
    *(stage for stages in _PROFILE_STAGES.values() for stage in stages)
) | {"REST_API"}


def _build_profile_automaton(
    stages: Sequence[Set[str]],
    optional_rest_api: bool = False,
    optional_stage_indexes: Set[int] | None = None,
) -> DeterministicFiniteAutomaton:
    automaton = DeterministicFiniteAutomaton()
    automaton.add_start_state(0)
    optional_stage_indexes = optional_stage_indexes or set()

    for index, stage in enumerate(stages):
        current_state = index
        next_state = index + 1
        for token in stage:
            automaton.add_transition(current_state, token, next_state)
            automaton.add_transition(next_state, token, next_state)

        if index in optional_stage_indexes and index + 1 < len(stages):
            for token in stages[index + 1]:
                automaton.add_transition(current_state, token, current_state + 2)

    final_state = len(stages)
    if optional_rest_api:
        database_state = 4
        automaton.add_transition(database_state, "REST_API", database_state)

    automaton.add_final_state(final_state)
    return automaton


_AUTOMATA = {
    profile: _build_profile_automaton(
        stages,
        optional_rest_api=(profile == "FULL_STACK"),
        optional_stage_indexes={1} if profile == "DATA_ENGINEER" else None,
    )
    for profile, stages in _PROFILE_STAGES.items()
}


def _evaluate_profile(qualifications: Iterable[str], profile: str) -> str:
    sequence = list(qualifications)
    if not sequence or any(token not in _KNOWN_TOKENS for token in sequence):
        return REJECTED
    return ACCEPTED if _AUTOMATA[profile].accepts(sequence) else REJECTED


def evaluate_full_stack(qualifications: Iterable[str]) -> str:
    return _evaluate_profile(qualifications, "FULL_STACK")


def evaluate_ml_engineer(qualifications: Iterable[str]) -> str:
    return _evaluate_profile(qualifications, "ML_ENGINEER")


def evaluate_devops_engineer(qualifications: Iterable[str]) -> str:
    return _evaluate_profile(qualifications, "DEVOPS_ENGINEER")


def evaluate_data_engineer(qualifications: Iterable[str]) -> str:
    return _evaluate_profile(qualifications, "DATA_ENGINEER")


def evaluate_all_profiles(qualifications: Iterable[str]) -> dict:
    sequence = list(qualifications)
    return {
        "FULL_STACK": evaluate_full_stack(sequence),
        "ML_ENGINEER": evaluate_ml_engineer(sequence),
        "DEVOPS_ENGINEER": evaluate_devops_engineer(sequence),
        "DATA_ENGINEER": evaluate_data_engineer(sequence),
    }