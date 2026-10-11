import html
import re
from pathlib import Path
from typing import Any


def _require_profile(profile: Any) -> None:
    if profile is None or not hasattr(profile, "name"):
        raise ValueError("A parsed candidate profile is required.")


def _profile_filename(name: str, suffix: str) -> str:
    name_parts = name.casefold().split()
    slug = re.sub(r"[^a-z0-9]+", "_", "_".join(name_parts[:2])).strip("_")
    return f"{slug or 'candidate'}_profile.{suffix}"


def generate_html_visualization(profile: Any) -> Path:
    _require_profile(profile)
    contact = profile.contact
    education = "".join(
        f"<li>{html.escape(record.degree)}</li>"
        for record in getattr(profile, "education", [])
    )
    experience = "".join(
        "<li><strong>{}</strong> — {}</li>".format(
            html.escape(record.title), html.escape(record.company)
        )
        for record in getattr(profile, "experience", [])
    )
    qualifications = "".join(
        f"<li>{html.escape(item)}</li>" for item in profile.qualifications
    )
    evaluations = "".join(
        "<li>{}: {}</li>".format(
            html.escape(str(item.profile)), html.escape(str(item.status))
        )
        for item in profile.evaluations
    )
    phone = getattr(contact, "phone", None)
    phone_html = f"<p>Phone: {html.escape(phone)}</p>" if phone else ""
    document = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{html.escape(profile.name)} - Resume</title></head>
<body>
  <main>
    <h1>{html.escape(profile.name)}</h1>
    <section><h2>Contact</h2><p>Email: {html.escape(contact.email)}</p>{phone_html}</section>
    <section><h2>Experience</h2><p>{profile.experience_years} years</p><ul>{experience}</ul></section>
    <section><h2>Education</h2><ul>{education}</ul></section>
    <section><h2>Qualifications</h2><ul>{qualifications}</ul></section>
    <section><h2>Profile evaluations</h2><ul>{evaluations}</ul></section>
  </main>
</body>
</html>
"""
    output_path = Path(_profile_filename(profile.name, "html"))
    output_path.write_text(document, encoding="utf-8")
    return output_path


def generate_markdown_visualization(profile: Any) -> Path:
    _require_profile(profile)
    contact = profile.contact
    lines = [
        f"# {profile.name}",
        "",
        "## Contact",
        f"- Email: {contact.email}",
    ]
    phone = getattr(contact, "phone", None)
    if phone:
        lines.append(f"- Phone: {phone}")
    lines.extend(
        [
            "",
            "## Experience",
            f"- Years of experience: {profile.experience_years}",
            "",
            "## Education",
        ]
    )
    lines.extend(
        f"- {record.degree}" for record in getattr(profile, "education", [])
    )
    lines.extend(
        [
            "",
            "## Work history",
            "| Title | Company |",
            "| --- | --- |",
        ]
    )
    lines.extend(
        f"| {record.title} | {record.company} |"
        for record in getattr(profile, "experience", [])
    )
    lines.extend(["", "## Qualifications"])
    lines.extend(f"- {item}" for item in profile.qualifications)
    lines.extend(["", "## Profile evaluations"])
    lines.extend(
        f"- {item.profile}: **{item.status}**" for item in profile.evaluations
    )

    output_path = Path(_profile_filename(profile.name, "md"))
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path