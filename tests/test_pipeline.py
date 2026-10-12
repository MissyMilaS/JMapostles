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
        self.assertEqual(result["profile_results"]["ML_ENGINEER"], "REJECTED")

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
        self.assertEqual(result["profile_results"]["FULL_STACK"], "REJECTED")

    def test_devops_profile_is_sorted_and_classified(self):
        resume = """Jordan Lee
WORK EXPERIENCE
4 years of experience managing cloud infrastructure.
Technical Skills: Git, Kubernetes, AWS, Python, Docker."""

        result = process_resume_pipeline(resume, profile="DEVOPS_ENGINEER")

        self.assertEqual(
            result["normalized_skills"],
            ["PYTHON", "DOCKER", "KUBERNETES", "AWS", "GIT"],
        )
        self.assertEqual(result["classification"], "ACCEPTED")
        self.assertEqual(result["profile_results"]["DEVOPS_ENGINEER"], "ACCEPTED")

    def test_data_profile_is_sorted_and_classified(self):
        resume = """Ada Lovelace
WORK EXPERIENCE
3 years of experience building data pipelines.
Technical Skills: Git, Airflow, Postgres, Spark, Python."""

        result = process_resume_pipeline(resume, profile="DATA_ENGINEER")

        self.assertEqual(
            result["normalized_skills"],
            ["PYTHON", "SPARK", "AIRFLOW", "POSTGRESQL", "GIT"],
        )
        self.assertEqual(result["classification"], "ACCEPTED")
        self.assertEqual(result["profile_results"]["DATA_ENGINEER"], "ACCEPTED")


if __name__ == "__main__":
    unittest.main()
