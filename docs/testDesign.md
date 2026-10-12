## Configuration of the Scenarios (Stage 1: Information Extraction - Regular Expressions)

| Name | Class | Scenario |
|------|------|----------|
| setUp1 | InformationExtractorTest | Valid CV text in a structured plain format with emails, internationally formatted phone numbers, and profile URLs (GitHub/LinkedIn) |
| setUp2 | InformationExtractorTest | CV text with multiple mentions and variations of programming languages (e.g. JS, Javascript, TypeScript, Python) |
| setUp3 | InformationExtractorTest | CV text with mentions of frontend and backend frameworks/libraries in various styles (e.g. React.js, ReactJS, NodeJS, Spring Boot, Vue.js) |
| setUp4 | InformationExtractorTest | CV text with relational and NoSQL database engines (e.g. Postgres, PostgreSQL, MySQL, MongoDB) |
| setUp5 | InformationExtractorTest | CV text with Machine Learning and Artificial Intelligence libraries and frameworks (e.g. Scikit-learn, sklearn, TensorFlow, PyTorch, Pandas, NumPy) |
| setUp6 | InformationExtractorTest | CV text with version control tools, repositories, and DevOps tools (e.g. Git, GitHub, Docker, Kubernetes) |
| setUp7 | InformationExtractorTest | Text with academic degrees (Bachelor, B.S., Master) and years of experience expressed in words/numbers |
| setUp8 | InformationExtractorTest | Empty text string (`""`) |
| setUp9 | InformationExtractorTest | Plain narrative/noisy text with common words and no technical skills or contact information |
| setUp10 | InformationExtractorTest | Text with technical qualifications attached to punctuation marks or delimiters (e.g. `"JS, React.js; NodeJS/Postgres"`) |

---

## Test Case Design - InformationExtractor (Stage 1: Regular Expressions)

**Test Objective:** Validate the correct behavior of extraction methods using regular expressions (Python's `re` module) to capture technical and contact information from CV text.

| Class | Method | Scenario | Input Values | Expected Result |
|------|--------|----------|--------------|-----------------|
| InformationExtractorTest | extract_contact_info | setUp1 | `"Contact: wednesday@addams.com \| +1-555-0199 \| github.com/wednesday \| linkedin.com/in/wednesday"` | `{"emails": ["wednesday@addams.com"], "phones": ["+1-555-0199"], "urls": ["github.com/wednesday", "linkedin.com/in/wednesday"]}` |
| InformationExtractorTest | extract_contact_info | setUp8 | `""` | `{"emails": [], "phones": [], "urls": []}` |
| InformationExtractorTest | extract_contact_info | setUp9 | `"Enthusiastic software engineer with strong teamwork abilities."` | `{"emails": [], "phones": [], "urls": []}` |
| InformationExtractorTest | extract_programming_languages | setUp2 | `"Proficient in JS, Javascript, TypeScript, and Python 3.9."` | `["JS", "Javascript", "TypeScript", "Python"]` |
| InformationExtractorTest | extract_programming_languages | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_programming_languages | setUp9 | `"Responsible for daily customer support and project tracking."` | `[]` |
| InformationExtractorTest | extract_frameworks | setUp3 | `"Experience in React.js, ReactJS, NodeJS, Spring Boot and Vue.js."` | `["React.js", "ReactJS", "NodeJS", "Spring Boot", "Vue.js"]` |
| InformationExtractorTest | extract_frameworks | setUp10 | `"Skills: React.js/NodeJS."` | `["React.js", "NodeJS"]` |
| InformationExtractorTest | extract_frameworks | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_databases | setUp4 | `"Worked with Postgres, PostgreSQL, MySQL, and MongoDB databases."` | `["Postgres", "PostgreSQL", "MySQL", "MongoDB"]` |
| InformationExtractorTest | extract_databases | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_databases | setUp9 | `"Managed project schedules and internal communication."` | `[]` |
| InformationExtractorTest | extract_ml_libraries | setUp5 | `"Hands-on with Scikit-learn, sklearn, TensorFlow, PyTorch, Pandas and NumPy."` | `["Scikit-learn", "sklearn", "TensorFlow", "PyTorch", "Pandas", "NumPy"]` |
| InformationExtractorTest | extract_ml_libraries | setUp10 | `"Models developed using Scikit-learn/TensorFlow."` | `["Scikit-learn", "TensorFlow"]` |
| InformationExtractorTest | extract_ml_libraries | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_tools | setUp6 | `"Version control using Git, remote repositories on GitHub, and Docker containers."` | `["Git", "GitHub", "Docker"]` |
| InformationExtractorTest | extract_tools | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_tools | setUp9 | `"Facilitated team sync meetings twice a week."` | `[]` |
| InformationExtractorTest | extract_experience_and_education | setUp7 | `"B.S. in Computer Science. 3 years of experience developing web applications."` | `{"degree": "B.S. in Computer Science", "years_experience": 3}` |
| InformationExtractorTest | extract_experience_and_education | setUp8 | `""` | `{"degree": null, "years_experience": 0}` |
| InformationExtractorTest | extract_all_qualifications | setUp1 | `"Technical Skills: JS, React.js, NodeJS, Postgres, Git."` | `["JS", "React.js", "NodeJS", "Postgres", "Git"]` |
| InformationExtractorTest | extract_all_qualifications | setUp5 | `"Technical Skills: Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git."` | `["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "SQL", "Git"]` |
| InformationExtractorTest | extract_all_qualifications | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_all_qualifications | setUp9 | `"Good communication, leadership, and proactive problem solving."` | `[]` |

---

## Configuration of the Scenarios (Stage 2: Canonical Normalization and Ordering - FST)

| Name | Class | Scenario |
|------|------|----------|
| setUp11 | QualificationNormalizerTest | List of extracted qualifications with variations in programming language names (e.g. JS, Javascript -> JAVASCRIPT) |
| setUp12 | QualificationNormalizerTest | List of qualifications with syntactic variations of frontend and backend frameworks (e.g. React.js, ReactJS -> REACT; NodeJS, Node.js -> NODE_JS) |
| setUp13 | QualificationNormalizerTest | List of qualifications with different ways of naming database engines (e.g. Postgres, PostgreSQL -> POSTGRESQL) |
| setUp14 | QualificationNormalizerTest | List of qualifications with variants of Machine Learning libraries (e.g. sklearn, scikit learn, Scikit-learn -> SCIKIT_LEARN; Tensor Flow, TensorFlow -> TENSORFLOW) |
| setUp15 | QualificationNormalizerTest | List of qualifications with variations in version control and environment names (e.g. Git, github -> GIT) |
| setUp16 | QualificationNormalizerTest | List of qualifications with mixed valid variations for a Full Stack profile |
| setUp17 | QualificationNormalizerTest | List of qualifications with mixed valid variations for a Machine Learning Engineer profile |
| setUp18 | QualificationNormalizerTest | Empty input string or list (`[]`) received from the extraction stage |
| setUp19 | QualificationNormalizerTest | List of qualifications containing unknown symbols or values outside the input alphabet Σ of the transducer |
| setUp20 | QualificationNormalizerTest | Disordered qualifications aimed at the Full Stack Developer profile (requires ordering: Frontend -> Backend -> Database -> Version Control) |
| setUp21 | QualificationNormalizerTest | Disordered qualifications aimed at the Machine Learning Engineer profile (requires ordering: Language -> Data processing -> ML Framework -> Database -> Version Control) |
| setUp22 | QualificationNormalizerTest | List of qualifications already ordered according to the canonical order of the target profile |

---

## Test Case Design - QualificationNormalizer (Stage 2: Finite-State Transducers)

**Test Objective:** Validate the correct transformation of textual variants into unique canonical tokens by finite-state transducers (`pyformlang`) and the subsequent sorting of the resulting qualifications.

| Class | Method | Scenario | Input Values | Expected Result |
|------|--------|----------|--------------|-----------------|
| QualificationNormalizerTest | normalize_qualification | setUp11 | `"JS"` | `"JAVASCRIPT"` |
| QualificationNormalizerTest | normalize_qualification | setUp11 | `"Javascript"` | `"JAVASCRIPT"` |
| QualificationNormalizerTest | normalize_qualification | setUp12 | `"React.js"` | `"REACT"` |
| QualificationNormalizerTest | normalize_qualification | setUp12 | `"ReactJS"` | `"REACT"` |
| QualificationNormalizerTest | normalize_qualification | setUp12 | `"NodeJS"` | `"NODE_JS"` |
| QualificationNormalizerTest | normalize_qualification | setUp12 | `"Node.js"` | `"NODE_JS"` |
| QualificationNormalizerTest | normalize_qualification | setUp13 | `"Postgres"` | `"POSTGRESQL"` |
| QualificationNormalizerTest | normalize_qualification | setUp13 | `"PostgreSQL"` | `"POSTGRESQL"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"sklearn"` | `"SCIKIT_LEARN"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"scikit learn"` | `"SCIKIT_LEARN"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"Scikit-learn"` | `"SCIKIT_LEARN"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"Tensor Flow"` | `"TENSORFLOW"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"TensorFlow"` | `"TENSORFLOW"` |
| QualificationNormalizerTest | normalize_qualification | setUp15 | `"Git"` | `"GIT"` |
| QualificationNormalizerTest | normalize_qualification | setUp19 | `"UnknownTech"` | `UNKNOWN` (or discarded according to design rules) |
| QualificationNormalizerTest | normalize_sequence | setUp16 | `["JS", "React.js", "NodeJS", "Postgres", "Git"]` | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | normalize_sequence | setUp17 | `["Python", "pandas", "sklearn", "TensorFlow", "Postgres", "Git"]` | `["PYTHON", "PANDAS", "SCIKIT_LEARN", "TENSORFLOW", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | normalize_sequence | setUp18 | `[]` | `[]` |
| QualificationNormalizerTest | sort_canonical | setUp20 | `["Git", "NodeJS", "JS", "Postgres", "React.js"]`, `profile="FULL_STACK"` | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | sort_canonical | setUp21 | `["Git", "TensorFlow", "Python", "Pandas", "Postgres"]`, `profile="ML_ENGINEER"` | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | sort_canonical | setUp22 | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]`, `profile="FULL_STACK"` | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | sort_canonical | setUp18 | `[]`, `profile="FULL_STACK"` | `[]` |

---

## Configuration of the Scenarios (Stage 3: Pattern Recognition - Finite Automata)

| Name | Class | Scenario |
|------|------|----------|
| setUp23 | ProfilePatternRecognizerTest | Valid ordered canonical sequence for the Full Stack Developer profile (e.g. JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT) |
| setUp24 | ProfilePatternRecognizerTest | Valid ordered canonical sequence for the Machine Learning Engineer profile (e.g. PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, GIT) |
| setUp25 | ProfilePatternRecognizerTest | Valid ordered canonical sequence for Additional Profile 1 - Software Engineering (e.g. DevOps / Cloud Engineer: PYTHON, DOCKER, KUBERNETES, AWS, GIT) |
| setUp26 | ProfilePatternRecognizerTest | Valid ordered canonical sequence for Additional Profile 2 - AI/Data (e.g. Data Engineer: PYTHON, SPARK, AIRFLOW, POSTGRESQL, GIT) |
| setUp27 | ProfilePatternRecognizerTest | Incomplete sequence for Full Stack Developer missing the Backend or Database token |
| setUp28 | ProfilePatternRecognizerTest | Incomplete sequence for Machine Learning Engineer missing the ML/Data library |
| setUp29 | ProfilePatternRecognizerTest | Sequence with symbols outside the alphabet Σ of a specific profile automaton (e.g. ML tokens evaluated in the Full Stack automaton) |
| setUp30 | ProfilePatternRecognizerTest | Sequence that violates the strict canonical order required by the automaton of the profile |
| setUp31 | ProfilePatternRecognizerTest | Empty canonical qualification list (`[]`) |
| setUp32 | ProfilePatternRecognizerTest | Multiprofile evaluation: valid candidate sequence for ML Engineer tested simultaneously against all 4 automata |

---

## Test Case Design - ProfilePatternRecognizer (Stage 3: Finite Automata)

**Test Objective:** Validate classification of canonical sequences through finite automata (DFA/NFA in `pyformlang`), verifying that the acceptance state is determined precisely and that invalid sequences are rejected.

| Class | Method | Scenario | Input Values | Expected Result |
|------|--------|----------|--------------|-----------------|
| ProfilePatternRecognizerTest | evaluate_full_stack | setUp23 | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` | `ACCEPTED` |
| ProfilePatternRecognizerTest | evaluate_full_stack | setUp27 | `["JAVASCRIPT", "REACT", "GIT"]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_full_stack | setUp29 | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_full_stack | setUp31 | `[]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_ml_engineer | setUp24 | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]` | `ACCEPTED` |
| ProfilePatternRecognizerTest | evaluate_ml_engineer | setUp28 | `["PYTHON", "POSTGRESQL", "GIT"]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_ml_engineer | setUp29 | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_ml_engineer | setUp31 | `[]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_devops_engineer | setUp25 | `["PYTHON", "DOCKER", "KUBERNETES", "AWS", "GIT"]` | `ACCEPTED` |
| ProfilePatternRecognizerTest | evaluate_devops_engineer | setUp23 | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_data_engineer | setUp26 | `["PYTHON", "SPARK", "AIRFLOW", "POSTGRESQL", "GIT"]` | `ACCEPTED` |
| ProfilePatternRecognizerTest | evaluate_data_engineer | setUp24 | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_all_profiles | setUp32 | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]` | `{"FULL_STACK": "REJECTED", "ML_ENGINEER": "ACCEPTED", "DEVOPS_ENGINEER": "REJECTED", "DATA_ENGINEER": "REJECTED"}` |
| ProfilePatternRecognizerTest | evaluate_all_profiles | setUp30 | `["REACT", "JAVASCRIPT", "NODE_JS", "POSTGRESQL", "GIT"]` | `{"FULL_STACK": "REJECTED", "ML_ENGINEER": "REJECTED", "DEVOPS_ENGINEER": "REJECTED", "DATA_ENGINEER": "REJECTED"}` |

---

## Configuration of the Scenarios (Stage 4: Profile Language and DSL - Context-Free Grammars with textX)

| Name | Class | Scenario |
|------|------|----------|
| setUp33 | ProfileDSLParserTest | Valid DSL specification file containing personal data, multiple work experiences, normalized technical skills, and accepted profile classifications |
| setUp34 | ProfileDSLParserTest | Valid DSL file for a candidate with multiple education records, multiple jobs, and several accepted classifications simultaneously |
| setUp35 | ProfileDSLParserTest | Invalid DSL file due to missing required sections (e.g. missing contact information block or missing profile classification block) |
| setUp36 | ProfileDSLParserTest | Invalid DSL file due to syntactic/lexical errors (e.g. unclosed quotes, incorrect delimiters, or misspelled keywords not recognized by the grammar) |
| setUp37 | ProfileDSLParserTest | Invalid DSL file with inconsistent data types (e.g. years of experience expressed as text instead of the required integer value) |
| setUp38 | ProfileDSLParserTest | Successful generation of an HTML visualization document from the parsed and validated DSL model in `textX` |
| setUp39 | ProfileDSLParserTest | Successful generation of a Markdown visualization document from the parsed and validated DSL model in `textX` |
| setUp40 | ProfileDSLParserTest | Attempt to generate visualization output (HTML/Markdown) from an unvalidated or corrupted AST/model |

---

## Test Case Design - ProfileDSLParser & Renderer (Stage 4: Context-Free Grammars with textX)

**Test Objective:** Validate the syntactic and lexical parsing of the domain-specific language (DSL) using context-free grammars in `textX`, verify correct error detection, and confirm generation of valid display documents and output files.

| Class | Method | Scenario | Input Values | Expected Result |
|------|--------|----------|--------------|-----------------|
| ProfileDSLParserTest | parse_dsl_string | setUp33 | Well-structured DSL string with candidate "Wednesday Addams", 3 years of experience, normalized skills, and classification `FULL_STACK: ACCEPTED` | Model object successfully parsed and validated |
| ProfileDSLParserTest | parse_dsl_string | setUp34 | Complete DSL string with 2 work experiences, B.S. in CS, and normalized items with multiple valid classifications | Model object successfully parsed and validated |
| ProfileDSLParserTest | parse_dsl_string | setUp35 | DSL string where the mandatory `evaluations` section is missing | Raises `TextXSyntaxError` indicating a missing required element |
| ProfileDSLParserTest | parse_dsl_string | setUp36 | DSL string with erroneous key `"CandidateProfile_BadSyntax { ... }"` | Raises `TextXSyntaxError` due to unrecognized rule |
| ProfileDSLParserTest | parse_dsl_string | setUp37 | DSL string with `experience_years = "three"` (an integer was expected) | Raises `TextXSemanticError` or `TextXSyntaxError` due to invalid data type |
| ProfileDSLParserTest | generate_html_visualization | setUp38 | Valid model object `CandidateProfile` processed from `setUp33` | Generates `wednesday_addams_profile.html` successfully |
| ProfileDSLParserTest | generate_markdown_visualization | setUp39 | Valid model object `CandidateProfile` processed from `setUp34` | Generates `mary_jane_profile.md` with the expected structure |
| ProfileDSLParserTest | generate_html_visualization | setUp40 | `None` or an unparsed DSL model | Raises `ValueError` or `AttributeError` preventing output generation |
