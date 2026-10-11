import os
import tempfile
import unittest
from pathlib import Path

from src.dsl import validator, visualizer


VALID_WEDNESDAY_PROFILE = """
CandidateProfile {
    name = "Wednesday Addams"
    contact = {
        email = "wednesday@addams.com"
        phone = "+1-555-0199"
    }
    experience_years = 3
    qualifications = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    evaluations = [FULL_STACK: ACCEPTED, ML_ENGINEER: REJECTED]
}
"""

VALID_MARY_PROFILE = """
CandidateProfile {
    name = "Mary Jane Watson"
    contact = {
        email = "mary.jane@example.com"
        phone = "+1-555-0100"
    }
    experience_years = 5
    education = [
        {degree = "B.S. in Computer Science"},
        {degree = "M.S. in Software Engineering"}
    ]
    experience = [
        {company = "Daily Bugle", title = "Software Engineer"},
        {company = "Parker Industries", title = "Senior Engineer"}
    ]
    qualifications = ["PYTHON", "DOCKER", "KUBERNETES", "AWS", "GIT"]
    evaluations = [DEVOPS_ENGINEER: ACCEPTED, FULL_STACK: ACCEPTED]
}
"""

MISSING_EVALUATIONS_PROFILE = """
CandidateProfile {
    name = "Wednesday Addams"
    contact = {email = "wednesday@addams.com"}
    experience_years = 3
    qualifications = ["JAVASCRIPT"]
}
"""

MISSING_CONTACT_PROFILE = """
CandidateProfile {
    name = "Wednesday Addams"
    experience_years = 3
    qualifications = ["JAVASCRIPT"]
    evaluations = [FULL_STACK: REJECTED]
}
"""

MALFORMED_PROFILE = 'CandidateProfile_BadSyntax { name = "Wednesday Addams" }'

UNCLOSED_STRING_PROFILE = """
CandidateProfile {
    name = "Wednesday Addams
    contact = {email = "wednesday@addams.com"}
    experience_years = 3
    qualifications = []
    evaluations = [FULL_STACK: REJECTED]
}
"""

INVALID_DELIMITER_PROFILE = """
CandidateProfile {
    name = "Wednesday Addams"
    contact = {email = "wednesday@addams.com"}
    experience_years = 3
    qualifications = ["JAVASCRIPT"
    evaluations = [FULL_STACK: REJECTED]
}
"""

INVALID_EXPERIENCE_PROFILE = """
CandidateProfile {
    name = "Wednesday Addams"
    contact = {email = "wednesday@addams.com"}
    experience_years = "tres"
    qualifications = []
    evaluations = [FULL_STACK: REJECTED]
}
"""


class TestProfileDSLParser(unittest.TestCase):
    def assert_textx_error(self, text):
        with self.assertRaises(Exception) as context:
            validator.parse_dsl_string(text)
        self.assertIn(
            type(context.exception).__name__,
            {"TextXSyntaxError", "TextXSemanticError"},
        )

    def test_parse_dsl_string_valid_single_candidate(self):
        with self.subTest(scenario="setUp33"):
            model = validator.parse_dsl_string(VALID_WEDNESDAY_PROFILE)
            self.assertIsNotNone(model)
            self.assertEqual(type(model).__name__, "CandidateProfile")
            self.assertEqual(model.name, "Wednesday Addams")
            self.assertEqual(model.experience_years, 3)
            self.assertEqual(
                model.qualifications,
                ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
            )
            self.assertEqual(len(model.evaluations), 2)

    def test_parse_dsl_string_valid_multiple_records(self):
        with self.subTest(scenario="setUp34"):
            model = validator.parse_dsl_string(VALID_MARY_PROFILE)
            self.assertIsNotNone(model)
            self.assertEqual(type(model).__name__, "CandidateProfile")
            self.assertEqual(model.name, "Mary Jane Watson")
            self.assertEqual(model.experience_years, 5)
            self.assertEqual(len(model.experience), 2)
            self.assertEqual(len(model.education), 2)
            self.assertEqual(len(model.evaluations), 2)

    def test_parse_dsl_string_rejects_missing_required_section(self):
        scenarios = (
            ("missing evaluations", MISSING_EVALUATIONS_PROFILE),
            ("missing contact", MISSING_CONTACT_PROFILE),
        )

        for scenario, text in scenarios:
            with self.subTest(scenario="setUp35", missing=scenario):
                self.assert_textx_error(text)

    def test_parse_dsl_string_rejects_bad_syntax(self):
        scenarios = (
            ("unknown root rule", MALFORMED_PROFILE),
            ("unclosed string", UNCLOSED_STRING_PROFILE),
            ("invalid delimiter", INVALID_DELIMITER_PROFILE),
        )

        for scenario, text in scenarios:
            with self.subTest(scenario="setUp36", syntax_error=scenario):
                self.assert_textx_error(text)

    def test_parse_dsl_string_rejects_invalid_experience_type(self):
        with self.subTest(scenario="setUp37"):
            self.assert_textx_error(INVALID_EXPERIENCE_PROFILE)

    def test_generate_html_visualization(self):
        with self.subTest(scenario="setUp38"):
            model = validator.parse_dsl_string(VALID_WEDNESDAY_PROFILE)
            previous_directory = os.getcwd()

            with tempfile.TemporaryDirectory() as output_directory:
                try:
                    os.chdir(output_directory)
                    visualizer.generate_html_visualization(model)
                    output_path = Path("wednesday_addams_profile.html")
                    self.assertTrue(output_path.is_file())
                    html = output_path.read_text(encoding="utf-8")
                    self.assertIn("<html", html.lower())
                    self.assertIn("Wednesday Addams", html)
                    self.assertIn("ACCEPTED", html)
                finally:
                    os.chdir(previous_directory)

    def test_generate_markdown_visualization(self):
        with self.subTest(scenario="setUp39"):
            model = validator.parse_dsl_string(VALID_MARY_PROFILE)
            previous_directory = os.getcwd()

            with tempfile.TemporaryDirectory() as output_directory:
                try:
                    os.chdir(output_directory)
                    visualizer.generate_markdown_visualization(model)
                    output_path = Path("mary_jane_profile.md")
                    self.assertTrue(output_path.is_file())
                    markdown = output_path.read_text(encoding="utf-8")
                    self.assertIn("Mary Jane Watson", markdown)
                    self.assertIn("|", markdown)
                    self.assertIn("DEVOPS_ENGINEER", markdown)
                finally:
                    os.chdir(previous_directory)

    def test_generate_html_visualization_rejects_unparsed_model(self):
        with self.subTest(scenario="setUp40"):
            with self.assertRaises((ValueError, AttributeError)):
                visualizer.generate_html_visualization(None)


if __name__ == "__main__":
    unittest.main()