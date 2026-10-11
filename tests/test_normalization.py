import unittest

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
            ("FullStack", "TypeScript", "TYPESCRIPT"),
            ("FullStack", "Angular", "ANGULAR"),
            ("FullStack", "Vue.js", "VUE"),
            ("FullStack", "Django", "DJANGO"),
            ("FullStack", "Spring Boot", "SPRING_BOOT"),
            ("setUp13", "Postgres", "POSTGRESQL"),
            ("setUp13", "PostgreSQL", "POSTGRESQL"),
            ("FullStack", "MySQL", "MYSQL"),
            ("FullStack", "MongoDB", "MONGODB"),
            ("FullStack", "SQL", "SQL"),
            ("FullStack", "NoSQL", "NOSQL"),
            ("FullStack", "RESTful APIs", "REST_API"),
            ("setUp14", "sklearn", "SCIKIT_LEARN"),
            ("setUp14", "scikit learn", "SCIKIT_LEARN"),
            ("setUp14", "Scikit-learn", "SCIKIT_LEARN"),
            ("setUp14", "Tensor Flow", "TENSORFLOW"),
            ("setUp14", "TensorFlow", "TENSORFLOW"),
            ("setUp15", "Git", "GIT"),
            ("setUp15", "github", "GIT"),
        )

        for scenario, qualification, expected in scenarios:
            with self.subTest(scenario=scenario, qualification=qualification):
                self.assertEqual(
                    fst_normalizer.normalize_qualification(qualification), expected
                )

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
                "FullStack alternatives",
                [
                    "TypeScript",
                    "Angular",
                    "Spring Boot",
                    "MongoDB",
                    "REST APIs",
                    "Git",
                ],
                [
                    "TYPESCRIPT",
                    "ANGULAR",
                    "SPRING_BOOT",
                    "MONGODB",
                    "REST_API",
                    "GIT",
                ],
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

    def test_normalize_canonical_tokens_idempotently(self):
        canonical_skills = [
            "JAVASCRIPT",
            "TYPESCRIPT",
            "REACT",
            "ANGULAR",
            "VUE",
            "NODE_JS",
            "DJANGO",
            "SPRING_BOOT",
            "POSTGRESQL",
            "MYSQL",
            "MONGODB",
            "SQL",
            "NOSQL",
            "REST_API",
            "GIT",
        ]

        self.assertEqual(
            fst_normalizer.normalize_sequence(canonical_skills), canonical_skills
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