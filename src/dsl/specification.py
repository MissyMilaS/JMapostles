import json
from pathlib import Path
from typing import Any, Mapping

from src.dsl.validator import parse_dsl_string
from src.dsl.visualizer import generate_html_visualization


_PROFILE_NAMES = {
    "FULL_STACK": "FULL_STACK_DEVELOPER",
    "FULL_STACK_DEVELOPER": "FULL_STACK_DEVELOPER",
    "ML_ENGINEER": "MACHINE_LEARNING_ENGINEER",
    "MACHINE_LEARNING_ENGINEER": "MACHINE_LEARNING_ENGINEER",
    "DEVOPS_ENGINEER": "SOFTWARE_ENGINEER",
    "SOFTWARE_ENGINEER": "SOFTWARE_ENGINEER",
    "DATA_ENGINEER": "DATA_ENGINEER",
}


def _contact_value(contact: Mapping[str, Any], key: str) -> str:
    value = contact.get(key)
    if value is None:
        alternatives = contact.get(f"{key}s", [])
        value = alternatives[0] if alternatives else ""
    if isinstance(value, list):
        value = value[0] if value else ""
    return str(value).strip()


def _experience_records(data: Mapping[str, Any]) -> list[tuple[str, int]]:
    records = data.get("experience_records")
    if records is not None:
        return [
            (str(record["role"]), int(record["years"]))
            for record in records
        ]

    experience = str(data.get("experience", "")).strip()
    if not experience or experience.casefold() == "experience not specified.":
        return []
    return [(experience, int(data.get("years_experience", 0)))]


def candidate_dsl_from_data(data: Mapping[str, Any]) -> str:
    """Serialize the normalized pipeline result as a ResumeLens candidate DSL."""
    name = str(data.get("candidate_name", data.get("name", ""))).strip()
    contact = data.get("contact_info", {})
    if not isinstance(contact, Mapping):
        raise ValueError("Structured contact information must be a mapping.")

    skills = data.get("normalized_skills", data.get("canonical_skills", []))
    evaluations = data.get("profile_results", data.get("profile_evaluations", {}))
    if not isinstance(evaluations, Mapping):
        raise ValueError("Profile evaluations must be a mapping.")

    dsl_lines = [
        f"candidate {json.dumps(name, ensure_ascii=False)} {{",
        "    contact {",
        f"        email: {json.dumps(_contact_value(contact, 'email'), ensure_ascii=False)}",
        f"        phone: {json.dumps(_contact_value(contact, 'phone'), ensure_ascii=False)}",
        "    }",
    ]
    experience_records = _experience_records(data)
    if experience_records:
        dsl_lines.append("    experience {")
        dsl_lines.extend(
            f"        role: {json.dumps(role, ensure_ascii=False)} years: {years}"
            for role, years in experience_records
        )
        dsl_lines.append("    }")

    dsl_lines.extend(["    skills {", "        " + ", ".join(map(str, skills)), "    }"])
    dsl_lines.append("    classification {")
    normalized_evaluations = {
        _PROFILE_NAMES[key]: str(status)
        for key, status in evaluations.items()
        if key in _PROFILE_NAMES
    }
    for profile_name in (
        "FULL_STACK_DEVELOPER",
        "MACHINE_LEARNING_ENGINEER",
        "SOFTWARE_ENGINEER",
        "DATA_ENGINEER",
    ):
        status = normalized_evaluations.get(profile_name)
        if status is not None:
            dsl_lines.append(f"        {profile_name}: {status}")
    dsl_lines.extend(["    }", "}"])
    return "\n".join(dsl_lines) + "\n"


def generate_candidate_profile(
    data: Mapping[str, Any], output_dir: str | Path
) -> dict[str, Any]:
    """Validate structured pipeline data and write its DSL and HTML report."""
    dsl_text = candidate_dsl_from_data(data)
    profile = parse_dsl_string(dsl_text)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    slug = Path(
        generate_html_visualization(profile, output_dir=output_path).name
    ).stem.removesuffix("_profile")
    specification_path = output_path / f"{slug}_profile.resume"
    specification_path.write_text(dsl_text, encoding="utf-8")

    html_path = output_path / f"{slug}_profile.html"
    return {
        "dsl": dsl_text,
        "profile": profile,
        "specification_path": specification_path,
        "html_path": html_path,
    }
