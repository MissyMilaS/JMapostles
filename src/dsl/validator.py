import re
from pathlib import Path
from typing import Any

from textx import metamodel_from_file
from textx.exceptions import TextXSemanticError


_EMAIL_PATTERN = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
_PHONE_PATTERN = re.compile(r"^\+?[\d\s().-]+$")
_SKILL_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")
_PROFILE_NAMES = {
    "FULL_STACK_DEVELOPER",
    "MACHINE_LEARNING_ENGINEER",
    "SOFTWARE_ENGINEER",
    "DATA_ENGINEER",
}


def _validate_legacy_profile(profile: Any) -> None:
    if not profile.name.strip():
        raise TextXSemanticError("Candidate name cannot be empty.")
    if not _EMAIL_PATTERN.fullmatch(profile.contact.email):
        raise TextXSemanticError("Contact email is not valid.")
    if profile.experience_years < 0:
        raise TextXSemanticError("Experience years cannot be negative.")


def _validate_resume(profile: Any) -> None:
    if not profile.name.strip():
        raise TextXSemanticError("Candidate name cannot be empty.")
    if not _EMAIL_PATTERN.fullmatch(profile.contact.email):
        raise TextXSemanticError("Contact email is not valid.")
    phone = profile.contact.phone
    if not _PHONE_PATTERN.fullmatch(phone) or sum(character.isdigit() for character in phone) < 7:
        raise TextXSemanticError("Contact phone is not valid.")

    skill_names = list(profile.skills.skills)
    if not skill_names:
        raise TextXSemanticError("At least one normalized skill is required.")
    if any(not _SKILL_PATTERN.fullmatch(skill) for skill in skill_names):
        raise TextXSemanticError("Skills must be uppercase normalized identifiers.")
    if len(skill_names) != len(set(skill_names)):
        raise TextXSemanticError("Normalized skills cannot be duplicated.")

    evaluations = profile.classifications.evaluations
    evaluated_profiles = [str(item.profile) for item in evaluations]
    if len(evaluated_profiles) != len(set(evaluated_profiles)):
        raise TextXSemanticError("A profile can only be classified once.")
    if set(evaluated_profiles) != _PROFILE_NAMES:
        raise TextXSemanticError("All four supported profiles must be classified.")

    if profile.experience:
        for entry in profile.experience.entries:
            if not entry.role.strip():
                raise TextXSemanticError("Experience roles cannot be empty.")
            if entry.years < 0:
                raise TextXSemanticError("Experience years cannot be negative.")


def parse_dsl_string(dsl_text: str) -> Any:
    is_legacy_profile = dsl_text.lstrip().startswith("CandidateProfile")
    grammar_name = "resume_grammar.tx" if is_legacy_profile else "candidate_dsl.tx"
    grammar_path = Path(__file__).with_name(grammar_name)
    metamodel = metamodel_from_file(str(grammar_path))
    profile = metamodel.model_from_str(dsl_text)
    if is_legacy_profile:
        _validate_legacy_profile(profile)
    else:
        _validate_resume(profile)
    return profile


def parse_dsl_file(file_path: str | Path) -> Any:
    path = Path(file_path)
    return parse_dsl_string(path.read_text(encoding="utf-8"))