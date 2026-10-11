from typing import Any, Dict

from src.classification.profile_automata import (
    evaluate_data_engineer,
    evaluate_devops_engineer,
    evaluate_full_stack,
    evaluate_ml_engineer,
)
from src.extraction.regex_extractor import stage_1_extract_resume_data
from src.normalization.canonical_sorter import sort_canonical
from src.normalization.fst_normalizer import normalize_sequence


_PROFILE_EVALUATORS = {
    "FULL_STACK": evaluate_full_stack,
    "ML_ENGINEER": evaluate_ml_engineer,
    "DEVOPS_ENGINEER": evaluate_devops_engineer,
    "DATA_ENGINEER": evaluate_data_engineer,
}


def analyze_resume(raw_text: str) -> Dict[str, Any]:
    """Run extraction and profile analysis as distinct processing stages."""
    result = stage_1_extract_resume_data(raw_text)
    normalized = normalize_sequence(result["extracted_skills"])
    result["normalized_skills"] = normalized
    result["canonical_skills"] = sort_canonical(normalized, profile="FULL_STACK")
    result["profile_evaluations"] = {
        profile: evaluator(sort_canonical(normalized, profile=profile))
        for profile, evaluator in _PROFILE_EVALUATORS.items()
    }
    return result