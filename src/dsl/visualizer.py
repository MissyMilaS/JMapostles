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


def _output_path(profile: Any, suffix: str, output_dir: str | Path | None) -> Path:
    directory = Path(output_dir) if output_dir is not None else Path.cwd()
    directory.mkdir(parents=True, exist_ok=True)
    return directory / _profile_filename(profile.name, suffix)


def _resume_html(profile: Any) -> str:
    contact = profile.contact
    experience = "".join(
        "<tr><td>{}</td><td>{}</td></tr>".format(
            html.escape(entry.role), entry.years
        )
        for entry in (profile.experience.entries if profile.experience else [])
    )
    skills = "".join(
        f'<li class="skill-tag">{html.escape(skill)}</li>'
        for skill in profile.skills.skills
    )
    evaluations = "".join(
        '<li class="status {}"><span>{}</span><strong>{}</strong></li>'.format(
            "accepted" if str(item.status) == "ACCEPTED" else "rejected",
            html.escape(str(item.profile).replace("_", " ").title()),
            html.escape(str(item.status)),
        )
        for item in profile.classifications.evaluations
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(profile.name)} - ResumeLens</title>
  <style>
    body {{ font: 16px/1.5 system-ui, sans-serif; margin: 2rem auto; max-width: 900px; padding: 0 1rem; color: #202938; }}
    h1, h2 {{ color: #152238; }}
    section {{ border-top: 1px solid #d9e0e8; margin-top: 1.5rem; padding-top: 1rem; }}
    .skills {{ display: flex; flex-wrap: wrap; gap: .5rem; list-style: none; padding: 0; }}
    .skill-tag {{ background: #e8eef8; border-radius: 1rem; padding: .25rem .75rem; }}
    .status {{ display: flex; justify-content: space-between; max-width: 25rem; padding: .5rem; }}
    .accepted strong {{ color: #187044; }} .rejected strong {{ color: #596273; }}
    table {{ border-collapse: collapse; width: 100%; }} th, td {{ border: 1px solid #d9e0e8; padding: .5rem; text-align: left; }}
  </style>
</head>
<body>
  <main>
    <h1>{html.escape(profile.name)}</h1>
    <section><h2>Contact</h2><p>Email: {html.escape(contact.email)}</p><p>Phone: {html.escape(contact.phone)}</p></section>
    <section><h2>Experience</h2><table><thead><tr><th>Role</th><th>Years</th></tr></thead><tbody>{experience}</tbody></table></section>
    <section><h2>Normalized skills</h2><ul class="skills">{skills}</ul></section>
    <section><h2>Profile classification</h2><ul>{evaluations}</ul></section>
  </main>
</body>
</html>
"""


def _legacy_html(profile: Any) -> str:
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
    return f"""<!doctype html>
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


def generate_html_visualization(
    profile: Any, output_dir: str | Path | None = None
) -> Path:
    _require_profile(profile)
    document = (
        _resume_html(profile)
        if hasattr(profile, "classifications")
        else _legacy_html(profile)
    )
    output_path = _output_path(profile, "html", output_dir)
    output_path.write_text(document, encoding="utf-8")
    return output_path


def generate_markdown_visualization(
    profile: Any, output_dir: str | Path | None = None
) -> Path:
    _require_profile(profile)
    if hasattr(profile, "classifications"):
        return _generate_resume_markdown(profile, output_dir)

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

    output_path = _output_path(profile, "md", output_dir)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def _generate_resume_markdown(profile: Any, output_dir: str | Path | None) -> Path:
    lines = [
        f"# {profile.name}",
        "",
        "## Contact",
        f"- Email: {profile.contact.email}",
        f"- Phone: {profile.contact.phone}",
        "",
        "## Experience",
        "| Role | Years |",
        "| --- | ---: |",
    ]
    if profile.experience:
        lines.extend(
            f"| {entry.role} | {entry.years} |"
            for entry in profile.experience.entries
        )
    lines.extend(["", "## Normalized skills"])
    lines.extend(f"- {skill}" for skill in profile.skills.skills)
    lines.extend(["", "## Profile classification"])
    lines.extend(
        f"- {item.profile}: **{item.status}**"
        for item in profile.classifications.evaluations
    )

    output_path = _output_path(profile, "md", output_dir)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path