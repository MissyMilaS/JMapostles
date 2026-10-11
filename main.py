import json
from pathlib import Path

from src.extraction.reader import load_all_resumes
from src.extraction.regex_extractor import process_resume_to_short_cv

# Load resumes.
data = load_all_resumes("data/raw_data")

# Prepare the output directory.
processed_dir = Path("data/processed")
processed_dir.mkdir(parents=True, exist_ok=True)

# Process and save each resume.
for file_name, content in data.items():
    short_cv = process_resume_to_short_cv(content)
    output_path = processed_dir / f"{Path(file_name).stem}_processed.txt"
    output_path.write_text(short_cv["short_cv_text"], encoding="utf-8")
    structured_output_path = processed_dir / f"{Path(file_name).stem}_extracted.json"
    structured_output_path.write_text(
        json.dumps(short_cv, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"File: {file_name}")
    print(f"Processed CV saved to: {output_path}")
    print(f"Structured extraction saved to: {structured_output_path}")
    print("Extracted Short CV:")
    print(short_cv["short_cv_text"])