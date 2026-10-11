import unittest

from pyformlang.fst import FST

from src.normalization import canonical_sorter, fst_normalizer


class TestQualificationNormalizer(unittest.TestCase):
    def test_normalize_qualification(self):
        scenarios = (
            ("setUp11", "JS", "JAVASCRIPT"),
            ("setUp11", "Javascript", "JAVASCRIPT"),
            ("setUp12", "React.js", "REACT"),
            ("setUp12", "ReactJS", "REACT"),
            ("setUp12", "NodeJS", "NODE_JS"),
            ("setUp12", "Node.js", "NODE_JS"),
            ("setUp13", "Postgres", "POSTGRESQL"),
            ("setUp13", "PostgreSQL", "POSTGRESQL"),
            ("setUp14", "sklearn", "SCIKIT_LEARN"),
            ("setUp14", "scikit learn", "SCIKIT_LEARN"),
            ("setUp14", "Scikit-learn", "SCIKIT_LEARN"),
            ("setUp14", "Tensor Flow", "TENSORFLOW"),
            ("setUp14", "TensorFlow", "TENSORFLOW"),
            ("setUp15", "Git", "GIT"),
            ("setUp15", "github", "GITHUB"),
        )

        for scenario, qualification, expected in scenarios:
            with self.subTest(scenario=scenario, qualification=qualification):
                self.assertEqual(
                    fst_normalizer.normalize_qualification(qualification), expected
                )

    def test_qualification_transducers_are_pyformlang_fsts(self):
        self.assertTrue(fst_normalizer.QUALIFICATION_TRANSDUCERS)
        self.assertTrue(
            all(
                isinstance(transducer, FST)
                for transducer in fst_normalizer.QUALIFICATION_TRANSDUCERS.values()
            )
        )

        javascript = fst_normalizer.QUALIFICATION_TRANSDUCERS["JAVASCRIPT"]
        self.assertEqual(list(javascript.translate("js")), [["JAVASCRIPT"]])
        react = fst_normalizer.QUALIFICATION_TRANSDUCERS["REACT"]
        self.assertEqual(list(react.translate("react")), [["REACT"]])
        self.assertEqual(list(react.translate("react.js")), [["REACT"]])

    def test_normalize_unknown_qualification(self):
        with self.subTest(scenario="setUp19"):
            result = fst_normalizer.normalize_qualification("UnknownTech")
            self.assertIn(result, ("UNKNOWN", None))

    def test_normalize_sequence(self):
        scenarios = (
            (
                "setUp16",
                ["JS", "React.js", "NodeJS", "Postgres", "Git"],
                ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
            ),
            (
                "setUp17",
                ["Python", "pandas", "sklearn", "TensorFlow", "Postgres", "Git"],
                [
                    "PYTHON",
                    "PANDAS",
                    "SCIKIT_LEARN",
                    "TENSORFLOW",
                    "POSTGRESQL",
                    "GIT",
                ],
            ),
            ("setUp18", [], []),
        )

        for scenario, qualifications, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(
                    fst_normalizer.normalize_sequence(qualifications), expected
                )

    def test_sort_canonical(self):
        scenarios = (
            (
                "setUp20",
                ["Git", "NodeJS", "JS", "Postgres", "React.js"],
                "FULL_STACK",
                ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
            ),
            (
                "setUp21",
                ["Git", "TensorFlow", "Python", "Pandas", "Postgres"],
                "ML_ENGINEER",
                ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"],
            ),
            (
                "setUp22",
                ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
                "FULL_STACK",
                ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
            ),
            ("setUp18", [], "FULL_STACK", []),
        )

        for scenario, qualifications, profile, expected in scenarios:
            with self.subTest(scenario=scenario, profile=profile):
                self.assertEqual(
                    canonical_sorter.sort_canonical(qualifications, profile=profile),
                    expected,
                )


if __name__ == "__main__":
    unittest.main()