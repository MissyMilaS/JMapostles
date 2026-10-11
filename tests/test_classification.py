import unittest

from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from src.classification import profile_automata


class TestProfilePatternRecognizer(unittest.TestCase):
    FULL_STACK = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    ML_ENGINEER = ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]
    DEVOPS_ENGINEER = ["PYTHON", "DOCKER", "KUBERNETES", "AWS", "GIT"]
    DATA_ENGINEER = ["PYTHON", "SPARK", "AIRFLOW", "POSTGRESQL", "GIT"]

    def test_evaluate_full_stack(self):
        scenarios = (
            ("setUp23", self.FULL_STACK, "ACCEPTED"),
            ("setUp27", ["JAVASCRIPT", "REACT", "GIT"], "REJECTED"),
            ("setUp29", self.ML_ENGINEER, "REJECTED"),
            ("setUp31", [], "REJECTED"),
        )

        for scenario, qualifications, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(
                    profile_automata.evaluate_full_stack(qualifications), expected
                )

    def test_evaluate_ml_engineer(self):
        scenarios = (
            ("setUp24", self.ML_ENGINEER, "ACCEPTED"),
            ("setUp28", ["PYTHON", "POSTGRESQL", "GIT"], "REJECTED"),
            ("setUp29", self.FULL_STACK, "REJECTED"),
            ("setUp31", [], "REJECTED"),
        )

        for scenario, qualifications, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(
                    profile_automata.evaluate_ml_engineer(qualifications), expected
                )

    def test_evaluate_devops_engineer(self):
        scenarios = (
            ("setUp25", self.DEVOPS_ENGINEER, "ACCEPTED"),
            ("setUp23", self.FULL_STACK, "REJECTED"),
        )

        for scenario, qualifications, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(
                    profile_automata.evaluate_devops_engineer(qualifications),
                    expected,
                )

    def test_evaluate_data_engineer(self):
        scenarios = (
            ("setUp26", self.DATA_ENGINEER, "ACCEPTED"),
            ("setUp24", self.ML_ENGINEER, "REJECTED"),
        )

        for scenario, qualifications, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(
                    profile_automata.evaluate_data_engineer(qualifications), expected
                )

    def test_evaluate_all_profiles(self):
        scenarios = (
            (
                "setUp32",
                self.ML_ENGINEER,
                {
                    "FULL_STACK": "REJECTED",
                    "ML_ENGINEER": "ACCEPTED",
                    "DEVOPS_ENGINEER": "REJECTED",
                    "DATA_ENGINEER": "REJECTED",
                },
            ),
            (
                "setUp30",
                ["REACT", "JAVASCRIPT", "NODE_JS", "POSTGRESQL", "GIT"],
                {
                    "FULL_STACK": "REJECTED",
                    "ML_ENGINEER": "REJECTED",
                    "DEVOPS_ENGINEER": "REJECTED",
                    "DATA_ENGINEER": "REJECTED",
                },
            ),
        )

        for scenario, qualifications, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(
                    profile_automata.evaluate_all_profiles(qualifications), expected
                )

    def test_profile_automata_are_dfas(self):
        self.assertEqual(len(profile_automata.PROFILE_AUTOMATA), 4)
        self.assertTrue(
            all(
                isinstance(automaton, DeterministicFiniteAutomaton)
                for automaton in profile_automata.PROFILE_AUTOMATA.values()
            )
        )

    def test_profile_automata_reject_permutations_and_extra_qualifications(self):
        self.assertEqual(
            profile_automata.evaluate_full_stack(
                ["REACT", "JAVASCRIPT", "NODE_JS", "POSTGRESQL", "GIT"]
            ),
            "REJECTED",
        )
        self.assertEqual(
            profile_automata.evaluate_full_stack(
                self.FULL_STACK + ["PYTHON"]
            ),
            "REJECTED",
        )

    def test_unknown_profile_is_reported(self):
        with self.assertRaisesRegex(ValueError, "Unsupported professional profile"):
            profile_automata.evaluate_profile(self.FULL_STACK, "UNKNOWN_PROFILE")


if __name__ == "__main__":
    unittest.main()