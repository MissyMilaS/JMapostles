import tempfile
import unittest
from pathlib import Path

from textx.exceptions import TextXSemanticError, TextXSyntaxError

from src.dsl.specification import candidate_dsl_from_data, generate_candidate_profile
from src.dsl.validator import parse_dsl_string
from src.pipeline import process_resume_pipeline


VALID_PROFILE = """\
candidate "Wednesday Addams" {
    contact {
        email: "wednesday@nevermore.edu"
        phone: "+1-555-0192"
    }
    experience {
        role: "Web Developer" years: 3
        role: "Backend Developer" years: 2
    }
    skills {
        JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT
    }
    classification {
        FULL_STACK_DEVELOPER: ACCEPTED
        MACHINE_LEARNING_ENGINEER: REJECTED
        SOFTWARE_ENGINEER: REJECTED
        DATA_ENGINEER: REJECTED
    }
}
"""


class TestStageFourDSL(unittest.TestCase):
    def test_documented_dsl_parses_repeated_experience_and_skills(self):
        profile = parse_dsl_string(VALID_PROFILE)

        self.assertEqual(profile.name, "Wednesday Addams")
        self.assertEqual(len(profile.experience.entries), 2)
        self.assertEqual(
            profile.skills.skills,
            ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
        )
        self.assertEqual(len(profile.classifications.evaluations), 4)

    def test_rejects_missing_skill_separator(self):
        malformed = VALID_PROFILE.replace(
            "JAVASCRIPT, REACT", "JAVASCRIPT REACT"
        )
        with self.assertRaises(TextXSyntaxError):
            parse_dsl_string(malformed)

    def test_experience_section_is_optional(self):
        without_experience = VALID_PROFILE.replace(
            """    experience {
        role: "Web Developer" years: 3
        role: "Backend Developer" years: 2
    }
""",
            "",
        )

        profile = parse_dsl_string(without_experience)

        self.assertIsNone(profile.experience)

    def test_rejects_invalid_contact_and_missing_classification(self):
        invalid_email = VALID_PROFILE.replace(
            "wednesday@nevermore.edu", "not-an-email"
        )
        with self.assertRaises(TextXSemanticError):
            parse_dsl_string(invalid_email)

        missing_profile = VALID_PROFILE.replace(
            "        DATA_ENGINEER: REJECTED\n", ""
        )
        with self.assertRaises(TextXSemanticError):
            parse_dsl_string(missing_profile)

    def test_rejects_unknown_profile_enum(self):
        invalid_profile = VALID_PROFILE.replace(
            "FULL_STACK_DEVELOPER: ACCEPTED",
            "AI_SUPERVISOR: ACCEPTED",
        )
        with self.assertRaises(TextXSyntaxError):
            parse_dsl_string(invalid_profile)

    def test_serializes_pipeline_result_and_writes_validated_outputs(self):
        resume = """Wednesday Addams
Contact: wednesday@nevermore.edu | +1-555-0192
WORK EXPERIENCE
Web Developer | Nevermore Tech | 3 years of experience
Technical Skills: JavaScript, React, Node.js, PostgreSQL, Git."""
        pipeline_result = process_resume_pipeline(resume)
        dsl_text = candidate_dsl_from_data(pipeline_result)
        profile = parse_dsl_string(dsl_text)
        self.assertEqual(profile.name, "Wednesday Addams")
        self.assertEqual(profile.classifications.evaluations[0].status, "ACCEPTED")

        with tempfile.TemporaryDirectory() as output_directory:
            artifacts = generate_candidate_profile(pipeline_result, output_directory)
            self.assertTrue(Path(artifacts["specification_path"]).is_file())
            self.assertTrue(Path(artifacts["html_path"]).is_file())
            self.assertIn("<html", Path(artifacts["html_path"]).read_text().lower())


if __name__ == "__main__":
    unittest.main()
