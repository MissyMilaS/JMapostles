import unittest

from src.pipeline import process_resume_pipeline


class TestResumePipeline(unittest.TestCase):
    def test_stage_one_skills_are_normalized_and_sorted(self):
        resume = """Wednesday Addams
WORK EXPERIENCE
3 years of experience developing web applications.
Technical Skills: Git, NodeJS, JS, Postgres, React.js."""

        result = process_resume_pipeline(resume, profile="FULL_STACK")

        self.assertEqual(
            result["extracted_skills"],
            ["Git", "NodeJS", "JS", "Postgres", "React.js"],
        )
        self.assertEqual(
            result["normalized_skills"],
            ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
        )
        self.assertEqual(result["classification"], "ACCEPTED")
        self.assertEqual(result["profile_results"]["FULL_STACK"], "ACCEPTED")

    def test_pipeline_sorts_for_machine_learning_profile(self):
        resume = """Mary Jane Watson
WORK EXPERIENCE
2 years of experience developing predictive models.
Technical Skills: Git, TensorFlow, Python, Pandas, Postgres."""

        result = process_resume_pipeline(resume, profile="ML_ENGINEER")

        self.assertEqual(
            result["normalized_skills"],
            ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"],
        )
        self.assertEqual(result["classification"], "ACCEPTED")
        self.assertEqual(result["profile_results"]["ML_ENGINEER"], "ACCEPTED")


if __name__ == "__main__":
    unittest.main()
