from typing import Any, Dict, Optional

from src.extraction.regex_extractor import stage_1_extract_resume_data
from src.normalization.canonical_sorter import sort_canonical


def process_resume_pipeline(
    raw_text: str, profile: Optional[str] = "FULL_STACK"
) -> Dict[str, Any]:
    extracted_data = stage_1_extract_resume_data(raw_text)
    extracted_skills = extracted_data["extracted_skills"]

    return {
        **extracted_data,
        "normalized_skills": sort_canonical(extracted_skills, profile=profile),
    }