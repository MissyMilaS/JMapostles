import unittest

from src.extraction import regex_extractor


class TestInformationExtractor(unittest.TestCase):
    def test_extract_contact_info(self):
        scenarios = (
            (
                "setUp1",
                "Contact: wednesday@addams.com | +1-555-0199 | "
                "github.com/wednesday | linkedin.com/in/wednesday",
                {
                    "emails": ["wednesday@addams.com"],
                    "phones": ["+1-555-0199"],
                    "urls": [
                        "github.com/wednesday",
                        "linkedin.com/in/wednesday",
                    ],
                },
            ),
            ("setUp8", "", {"emails": [], "phones": [], "urls": []}),
            (
                "setUp9",
                "Enthusiastic software engineer with strong teamwork abilities.",
                {"emails": [], "phones": [], "urls": []},
            ),
        )

        for scenario, text, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(regex_extractor.extract_contact_info(text), expected)

    def test_extract_programming_languages(self):
        scenarios = (
            (
                "setUp2",
                "Proficient in JS, Javascript, TypeScript, and Python 3.9.",
                ["JS", "Javascript", "TypeScript", "Python"],
            ),
            ("setUp8", "", []),
            (
                "setUp9",
                "Responsible for daily customer support and project tracking.",
                [],
            ),
        )

        for scenario, text, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(
                    regex_extractor.extract_programming_languages(text), expected
                )

    def test_extract_frameworks(self):
        scenarios = (
            (
                "setUp3",
                "Experience in React.js, ReactJS, NodeJS, Spring Boot and Vue.js.",
                ["React.js", "ReactJS", "NodeJS", "Spring Boot", "Vue.js"],
            ),
            ("setUp10", "Skills: React.js/NodeJS.", ["React.js", "NodeJS"]),
            ("setUp8", "", []),
        )

        for scenario, text, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(regex_extractor.extract_frameworks(text), expected)

    def test_extract_databases(self):
        scenarios = (
            (
                "setUp4",
                "Worked with Postgres, PostgreSQL, MySQL, and MongoDB databases.",
                ["Postgres", "PostgreSQL", "MySQL", "MongoDB"],
            ),
            ("setUp8", "", []),
            (
                "setUp9",
                "Managed project schedules and internal communication.",
                [],
            ),
        )

        for scenario, text, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(regex_extractor.extract_databases(text), expected)

    def test_extract_ml_libraries(self):
        scenarios = (
            (
                "setUp5",
                "Hands-on with Scikit-learn, sklearn, TensorFlow, PyTorch, "
                "Pandas and NumPy.",
                ["Scikit-learn", "sklearn", "TensorFlow", "PyTorch", "Pandas", "NumPy"],
            ),
            (
                "setUp10",
                "Models developed using Scikit-learn/TensorFlow.",
                ["Scikit-learn", "TensorFlow"],
            ),
            ("setUp8", "", []),
        )

        for scenario, text, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(regex_extractor.extract_ml_libraries(text), expected)

    def test_extract_tools(self):
        scenarios = (
            (
                "setUp6",
                "Version control using Git, remote repositories on GitHub, "
                "and Docker containers.",
                ["Git", "GitHub", "Docker"],
            ),
            ("setUp8", "", []),
            ("setUp9", "Facilitated team sync meetings twice a week.", []),
        )

        for scenario, text, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(regex_extractor.extract_tools(text), expected)

    def test_extract_experience_and_education(self):
        scenarios = (
            (
                "setUp7",
                "B.S. in Computer Science. "
                "3 years of experience developing web applications.",
                {"degree": "B.S. in Computer Science", "years_experience": 3},
            ),
            (
                "setUp8",
                "",
                {"degree": None, "years_experience": 0},
            ),
        )

        for scenario, text, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(
                    regex_extractor.extract_experience_and_education(text), expected
                )

    def test_extract_all_qualifications(self):
        scenarios = (
            (
                "setUp1",
                "Technical Skills: JS, React.js, NodeJS, Postgres, Git.",
                ["JS", "React.js", "NodeJS", "Postgres", "Git"],
            ),
            (
                "setUp5",
                "Technical Skills: Python, Pandas, NumPy, Scikit-learn, "
                "TensorFlow, SQL, Git.",
                ["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "SQL", "Git"],
            ),
            ("setUp8", "", []),
            (
                "setUp9",
                "Good communication, leadership, and proactive problem solving.",
                [],
            ),
        )

        for scenario, text, expected in scenarios:
            with self.subTest(scenario=scenario):
                self.assertEqual(
                    regex_extractor.extract_all_qualifications(text), expected
                )


if __name__ == "__main__":
    unittest.main()