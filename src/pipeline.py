from typing import Any, Dict, Optional

from src.classification.profile_automata import (
    PROFILE_PATTERNS,
    evaluate_profile,
    normalize_profile_name,
)
from src.extraction.regex_extractor import stage_1_extract_resume_data
from src.normalization.canonical_sorter import sort_canonical


def process_resume_pipeline(
    raw_text: str, profile: Optional[str] = "FULL_STACK"
) -> Dict[str, Any]:
    profile_name = normalize_profile_name(profile)
    extracted_data = stage_1_extract_resume_data(raw_text)
    extracted_skills = extracted_data["extracted_skills"]
    normalized_skills = sort_canonical(extracted_skills, profile=profile_name)
    profile_results = {
        candidate_profile: evaluate_profile(
            sort_canonical(extracted_skills, profile=candidate_profile),
            candidate_profile,
        )
        for candidate_profile in PROFILE_PATTERNS
    }

    return {
        **extracted_data,
        "normalized_skills": normalized_skills,
        "profile_results": profile_results,
        "classification": profile_results[profile_name],
    }


def analyze_resume(raw_text: str) -> Dict[str, Any]:
    result = process_resume_pipeline(raw_text)
    return {**result,"canonical_skills": result["normalized_skills"],"profile_evaluations": result["profile_results"]}