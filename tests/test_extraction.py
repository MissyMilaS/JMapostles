import unittest

from src.extraction import regex_extractor
from src.pipeline import analyze_resume


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

    def test_extract_experience_section(self):
        experience_text = """Full Stack Developer | Nevermore Tech Solutions | Jan 2024 – Present
• Engineered multi-tier web applications using React.js for client-side rendering and NodeJS for server-side logic.
• Designed and optimized relational database schemas in Postgres, reducing complex query execution times by 35%.
• Integrated RESTful APIs and maintained strict version control workflows using Git in agile team environments."""
        resume = f"""Wednesday Addams
WORK EXPERIENCE
{experience_text}"""

        self.assertEqual(regex_extractor.extract_experience(resume), experience_text)
        processed_resume = regex_extractor.process_resume_to_short_cv(resume)
        self.assertEqual(processed_resume["experience"], experience_text)

    def test_extract_experience_section_from_single_line_resume(self):
        resume = """Wednesday Addams WORK EXPERIENCE Full Stack Developer | Nevermore Tech Solutions | Jan 2024 – Present • Engineered multi-tier web applications using React.js for client-side rendering and NodeJS for server-side logic. • Designed and optimized relational database schemas in Postgres, reducing complex query execution times by 35%. • Integrated RESTful APIs and maintained strict version control workflows using Git in agile team environments."""
        result = regex_extractor.process_resume_to_short_cv(resume)

        self.assertEqual(result["candidate_name"], "Wednesday Addams")
        self.assertNotEqual(result["experience"], "Experience not specified.")
        self.assertIn("Full Stack Developer", result["experience"])
        self.assertIn("Nevermore Tech Solutions", result["experience"])
        self.assertIn("client-side rendering", result["experience"])
        self.assertIn("Postgres", result["experience"])
        self.assertIn("version control workflows using Git", result["experience"])

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

    def test_extract_full_stack_alternative_technologies(self):
        resume = (
            "JavaScript TypeScript React Angular Vue Node.js Django Spring Boot "
            "SQL NoSQL PostgreSQL MySQL MongoDB REST APIs Git"
        )
        result = regex_extractor.stage_1_extract_resume_data(resume)

        self.assertEqual(
            set(result["extracted_skills"]),
            {
                "JavaScript",
                "TypeScript",
                "React",
                "Angular",
                "Vue",
                "Node.js",
                "Django",
                "Spring Boot",
                "SQL",
                "NoSQL",
                "PostgreSQL",
                "MySQL",
                "MongoDB",
                "REST APIs",
                "Git",
            },
        )
        self.assertNotIn("canonical_skills", result)
        analysis = analyze_resume(resume)
        self.assertIn("REST_API", analysis["canonical_skills"])
        self.assertIn("SPRING_BOOT", analysis["canonical_skills"])
        self.assertEqual(
            analysis["profile_evaluations"]["FULL_STACK"], "ACCEPTED"
        )

    def test_extracts_academics_experience_and_contact(self):
        resume = """Wednesday Addams
Contact: wednesday@addams.com | +1-555-0199
LinkedIn: https://linkedin.com/in/wednesday
EDUCATION
B.S. in Computer Science
WORK EXPERIENCE
Full Stack Developer | Nevermore Tech Solutions | Jan 2024 – Present
• Engineered multi-tier web applications using React.js for client-side rendering and NodeJS for server-side logic.
• Designed and optimized relational database schemas in Postgres, reducing complex query execution times by 35%.
• Integrated RESTful APIs and maintained strict version control workflows using Git in agile team environments.
"""
        result = regex_extractor.stage_1_extract_resume_data(resume)

        self.assertEqual(
            result["contact_info"],
            {
                "emails": ["wednesday@addams.com"],
                "phones": ["+1-555-0199"],
                "urls": ["https://linkedin.com/in/wednesday"],
            },
        )
        self.assertEqual(result["education"]["degree"], "B.S. in Computer Science")
        self.assertEqual(result["years_experience"], 0)
        self.assertIn("Full Stack Developer", result["experience"])
        self.assertEqual(result["programming_languages"], [])
        self.assertEqual(result["frameworks"], ["React.js", "NodeJS"])
        self.assertEqual(result["databases"], ["Postgres"])
        self.assertEqual(result["tools"], ["RESTful APIs", "Git"])
        self.assertIn("Full Stack Developer | Nevermore Tech Solutions", result["experience"])
        self.assertIn("client-side rendering", result["experience"])
        self.assertIn("35%", result["experience"])

    def test_stage_one_only_extracts_without_normalizing_or_classifying(self):
        result = regex_extractor.stage_1_extract_resume_data("JavaScript React Node.js")

        self.assertEqual(result["programming_languages"], ["JavaScript"])
        self.assertEqual(result["frameworks"], ["React", "Node.js"])
        self.assertNotIn("normalized_skills", result)
        self.assertNotIn("profile_evaluations", result)


if __name__ == "__main__":
    unittest.main()