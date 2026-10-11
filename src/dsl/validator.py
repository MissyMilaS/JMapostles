import re
from pathlib import Path
from typing import Any

from textx import metamodel_from_file
from textx.exceptions import TextXSemanticError


_EMAIL_PATTERN = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)


def _validate_profile(profile: Any) -> None:
    if not profile.name.strip():
        raise TextXSemanticError("Candidate name cannot be empty.")
    if not _EMAIL_PATTERN.fullmatch(profile.contact.email):
        raise TextXSemanticError("Contact email is not valid.")
    if profile.experience_years < 0:
        raise TextXSemanticError("Experience years cannot be negative.")


def parse_dsl_string(dsl_text: str) -> Any:
    grammar_path = Path(__file__).with_name("resume_grammar.tx")
    metamodel = metamodel_from_file(str(grammar_path))
    profile = metamodel.model_from_str(dsl_text)
    _validate_profile(profile)
    return profile


def parse_dsl_file(file_path: str | Path) -> Any:
    path = Path(file_path)
    return parse_dsl_string(path.read_text(encoding="utf-8"))