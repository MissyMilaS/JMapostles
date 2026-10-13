ResumeLens — AI Interaction Report

1. Introduction

This document records the use of Artificial Intelligence (AI) during the development of ResumeLens, a résumé-screening application developed for Computing and Discrete Structures III (2026-2).

The purpose of this report is to document the prompts used, the responses provided by AI, and the knowledge acquired during the development process.

AI was used as a collaborative tool to support the understanding of formal language theory, explore implementation strategies, improve software design, and identify possible testing scenarios.

The project applies four main computational models:

1. Regular Expressions for information extraction.
2. Finite-State Transducers for qualification normalization.
3. Finite Automata for professional profile recognition.
4. Context-Free Grammars using textX for candidate profile validation and visualization.

Note: The prompts and response summaries below are proposed documentation examples. They must be adjusted to reflect the actual interactions, responses, code, and results obtained during the project.

---

2. Goal 1 — Resume Information Extraction Using Regular Expressions

Objective: Extract relevant information from résumé text using regular expressions implemented with Python's "re" module.

Prompt| AI Response| What I Learned
Explain how to use Python regular expressions to extract programming languages, frameworks, libraries, databases, and development tools from résumé text. Provide examples and explain how the patterns work.| AI explained that regular expressions can identify textual patterns such as technology names, email addresses, and other relevant information. Python's "re" module provides functions such as "re.findall()" and "re.search()" to locate matching text.| I learned that regular expressions are useful for extracting information from unstructured text. Each expression must be designed according to the type of information being searched for.
How can I extract technology names from a résumé containing abbreviations such as JS, React.js, NodeJS, Postgres, and Git?| AI explained that extraction patterns can identify known technology names and return the matching strings. The extracted values can be stored in lists or dictionaries for subsequent processing.| I learned that extraction identifies the text present in the résumé but does not determine whether different expressions represent the same technology.
How should extracted information be stored so that it can be processed by the next module?| AI suggested organizing extracted values into structured data, such as lists, dictionaries, or other appropriate data structures.| I learned that the output of one module must be structured consistently so that it can be used as the input of the next stage.
What problems can occur when using regular expressions to extract résumé information?| AI identified possible false positives, unsupported abbreviations, variations in capitalization, and incomplete information as potential challenges.| I learned that regular expressions have limitations and must be tested with different résumé formats. A pattern that is too broad may extract irrelevant information, while a restrictive pattern may miss valid qualifications.

Goal 1 — Practical Example

Input:

Technical Skills:
JS, React.js, NodeJS, Postgres, Git.

Expected extraction:

JS
React.js
NodeJS
Postgres
Git

The extracted strings are then passed to Goal 2 for normalization.

---

3. Goal 2 — Qualification Normalization Using Finite-State Transducers

Objective: Transform different textual representations of equivalent qualifications into a common canonical representation using finite-state transducers implemented with "pyformlang".

Prompt| AI Response| What I Learned
Explain how finite-state transducers can normalize different representations of programming languages, frameworks, libraries, and databases.| AI explained that finite-state transducers process input symbols and produce output symbols or sequences. They can model transformations between different textual representations and standardized qualification names.| I learned that transducers are useful when equivalent qualifications appear under different names or abbreviations.
Explain the seven-tuple definition of a finite-state transducer: (M=(Q,\Sigma,\Gamma,\delta,\omega,q_0,F)).| AI described the components as the state set, input alphabet, output alphabet, transition relation, output relation, initial state, and accepting-state set.| I learned that a transducer must be formally defined, not merely described as a collection of text replacements.
How can I normalize JS, Javascript, React.js, ReactJS, NodeJS, and Postgres into canonical representations?| AI suggested defining transformations that map supported variants to common labels, such as JS to JAVASCRIPT, React.js to REACT, NodeJS to NODE_JS, and Postgres to POSTGRESQL.| I learned that normalization creates a consistent vocabulary for subsequent classification. The specific mappings must be supported by the implementation.
How can finite-state transducers be implemented using "pyformlang"?| AI explained that the implementation must define the transducer's states, initial and final states, transitions, and outputs using the library's supported interface.| I learned that a dictionary of replacements is not, by itself, a formal finite-state transducer. The theoretical model and its implementation must agree.
Why should normalized qualifications be organized in a consistent order?| AI explained that a canonical ordering can make qualification sequences consistent with the recognition patterns defined for each professional profile.| I learned that consistent ordering can simplify recognition, provided that the ordering rules are explicitly defined and applied consistently.

Goal 2 — Practical Example

Extracted Qualification| Expected Normalized Qualification
JS| JAVASCRIPT
React.js| REACT
NodeJS| NODE_JS
Postgres| POSTGRESQL
Git| GIT

The resulting normalized qualifications become the input for Goal 3.

---

4. Goal 3 — Qualification Pattern Recognition Using Finite Automata

Objective: Determine whether normalized qualifications satisfy the accepted pattern of a professional profile using finite automata implemented with "pyformlang".

Prompt| AI Response| What I Learned
Explain how finite automata can be used to recognize professional qualification patterns in ResumeLens.| AI explained that an automaton processes a sequence of symbols according to its states and transitions. It accepts or rejects the sequence depending on the resulting state and the set of accepting states.| I learned that classification can be modeled as a formal recognition process rather than an unexplained decision.
Explain the five-tuple definition of a finite automaton: (M=(Q,\Sigma,\delta,q_0,F)).| AI described the state set, alphabet, transition function or relation, initial state, and accepting-state set.| I learned that the formal definition establishes the structure and behavior of the recognition model.
How can a Full Stack Developer qualification pattern be represented using a finite automaton?| AI explained that normalized qualifications can be treated as input symbols and processed according to transitions representing the defined profile pattern.| I learned that the accepted qualification patterns must be explicitly defined. The automaton's behavior depends on its actual transitions and acceptance criteria.
How can a Machine Learning Engineer profile be recognized using an automaton?| AI explained that normalized qualifications such as PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, and GIT can be evaluated against the profile's formal recognition rules.| I learned that the recognition model must use the normalized output from Goal 2 and the qualification criteria established for the selected profile.
What test cases should be used to validate a profile-recognition automaton?| AI suggested testing accepted sequences, rejected sequences, missing qualifications, unsupported symbols, empty inputs, and different qualification orders.| I learned that testing should cover both valid and invalid cases. Expected results must be derived from the formal definition of the automaton.
How can four professional profiles be processed through the same application?| AI suggested using a shared processing pipeline with profile-specific recognition rules or automata.| I learned that the four profiles should reuse the general system architecture instead of requiring four independent applications.

Goal 3 — Example of Recognition

Input sequence:

PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, GIT

Example profile:

MACHINE_LEARNING_ENGINEER

Expected result according to the assignment example:

ACCEPTED

The actual implementation must be tested against the team's formal automaton definitions.

---

5. Goal 4 — Candidate Profile Language Using Context-Free Grammars and textX

Objective: Define and implement a domain-specific language for structured candidate profiles using a context-free grammar and the "textX" library.

Prompt| AI Response| What I Learned
Explain how context-free grammars can be used to define a structured language for candidate profiles.| AI explained that a grammar defines the syntactic rules of a language, including its valid structures and the relationships between its elements.| I learned that a grammar provides a formal specification for the structure of candidate information.
Explain how to define a candidate-profile grammar using EBNF, including terminals and non-terminals.| AI explained that terminals represent the basic symbols or tokens of the language, while non-terminals describe syntactic structures composed of other grammar elements.| I learned that EBNF provides a notation for documenting the structure of the candidate-profile language.
How can "textX" be used to implement and validate the candidate-profile grammar?| AI explained that "textX" can construct a parser from a grammar definition and use it to parse representations that follow the defined syntax.| I learned that the grammar must be implemented and tested to determine whether candidate profiles conform to the specified language.
How should the grammar represent personal information, contact information, education, experience, skills, and classification results?| AI suggested defining separate structural elements for candidate information, repeated education records, professional experiences, qualifications, and classification results.| I learned that a structured language should reflect the information produced by the previous processing stages and support repeated elements where necessary.
How can invalid candidate profiles be rejected?| AI explained that inputs that violate the grammar's lexical or syntactic rules should fail validation.| I learned that grammar validation helps prevent incorrectly structured information from being treated as a valid candidate profile.
How can a validated candidate profile be converted into a visualization?| AI suggested using the parsed candidate data to generate a Markdown or HTML representation after successful validation.| I learned that parsing and visualization are separate operations. The application should use structured, validated data to generate the final presentation.

Goal 4 — Expected Processing Flow

Candidate Information
        |
        v
Candidate Profile DSL
        |
        v
textX Parser
        |
        v
Grammar Validation
        |
        v
Structured Candidate Data
        |
        v
Markdown or HTML Visualization

---

6. AI Assistance in Architecture and Module Integration

Objective: Design a modular architecture that integrates the four formal models into a single application.

Prompt| AI Response| What I Learned
Propose a modular architecture for ResumeLens integrating regular expressions, finite-state transducers, finite automata, and context-free grammars.| AI suggested separating the application into modules for extraction, normalization, recognition, grammar validation, and visualization.| I learned that separating responsibilities makes the system easier to maintain, test, and understand.
Define the inputs and outputs of each module.| AI explained that each module should have a clear input-output contract. Extracted information feeds normalization, normalized qualifications feed recognition, and structured candidate information feeds grammar validation.| I learned that the interfaces between modules are important because each stage depends on the output of the previous stage.
How can the system support four professional profiles without duplicating the entire application?| AI suggested sharing the general pipeline while selecting the appropriate recognition model and profile-specific rules.| I learned that reusable components reduce duplication and help maintain consistency across the supported profiles.
How should errors between modules be handled?| AI suggested validating module outputs and checking whether the data received by the next stage follows the expected structure.| I learned that integration testing is necessary because individual modules may work independently but still fail when combined.

Architecture Summary

Component| Responsibility| Output
Information extraction| Identify relevant information in résumé text| Extracted information
Qualification normalization| Convert supported variants into canonical labels| Normalized qualifications
Profile recognition| Evaluate qualifications against a formal pattern| Recognition result
Grammar validation| Validate the structured candidate representation| Parsed candidate data
Visualization| Present validated information| Markdown or HTML output

---

7. AI Assistance in Testing and Debugging

Objective: Use AI to help identify possible errors, design test cases, and understand unexpected behavior during development.

Prompt| AI Response| What I Learned
Suggest test cases for the four ResumeLens processing stages, including valid inputs, invalid inputs, and edge cases.| AI suggested testing missing information, unsupported qualification names, invalid sequences, malformed candidate profiles, and inconsistencies between modules.| I learned that testing must cover more than normal inputs. Edge cases can reveal weaknesses in both the implementation and the formal models.
Explain how to investigate a Python error occurring in a ResumeLens module.| AI can help interpret the error message, identify possible causes, and suggest debugging steps based on the code and context provided.| I learned that error messages provide useful information, but the proposed explanation must be checked against the actual code and execution environment.
How can I determine whether an error originates in extraction, normalization, recognition, or grammar validation?| AI suggested inspecting the output of each stage and checking it against the expected input of the next component.| I learned that debugging is easier when modules have clearly defined responsibilities and their intermediate outputs can be inspected.
How can I verify that the application behaves according to the formal definitions?| AI suggested comparing observed outputs with the transition rules, normalization mappings, grammar rules, and expected test results.| I learned that software correctness must be evaluated against the specification rather than inferred from whether the application runs without errors.

---

8. Overall Learning Outcomes

Topic| What I Learned
Regular Expressions| Regular expressions extract relevant information from unstructured résumé text but do not perform semantic normalization or professional profile recognition.
Finite-State Transducers| Transducers model transformations from supported textual variants to canonical qualification representations.
Finite Automata| Automata recognize sequences according to formally defined states, transitions, and accepting states.
Context-Free Grammars| Grammars define the valid structure of the candidate-profile language and can be implemented using textX.
Software Architecture| A modular architecture separates responsibilities and enables the four formal models to work together in one application.
Testing| Test cases must be derived from the specifications and executed to verify actual behavior.
AI Collaboration| AI can support explanations, implementation ideas, debugging, and documentation, but its suggestions require critical evaluation and verification.
Technical Documentation| Recording prompts, responses, modifications, and learning outcomes makes the development process more transparent.

---

9. Critical Evaluation of AI Usage

AI was treated as a support tool rather than as a replacement for technical reasoning or implementation work.

Its main potential benefits included explaining theoretical concepts, suggesting implementation approaches, identifying possible edge cases, and helping organize technical documentation.

However, AI-generated suggestions can contain errors, omit assignment requirements, or propose solutions that do not match the project's implementation. Consequently, formal definitions, code examples, and expected outputs must be checked before they are included in the final application.

The project also requires a distinction between theoretical correctness and practical execution. A model may be described correctly but implemented incorrectly, or a program may run successfully without satisfying all the formal requirements.

For this reason, the final evaluation must be based on the assignment specification, the actual source code, and documented test results.

---

10. Final Reflection

The development of ResumeLens provides an opportunity to connect the theoretical concepts studied in Computing and Discrete Structures III with a practical software application.

Through the four project goals, I learned that different formal models solve different problems. Regular expressions extract information, finite-state transducers normalize representations, finite automata recognize qualification patterns, and context-free grammars validate structured candidate information.

AI collaboration can make these concepts easier to explore and can support implementation and documentation. Nevertheless, meaningful learning requires reviewing the responses, understanding the proposed solutions, modifying them when necessary, and verifying the final behavior.

The most important outcome is not simply obtaining code with AI assistance. It is understanding why each formal model is used, how it works, how it connects to the other components, and how its behavior can be demonstrated through tests.

---

11. Evidence and Completion Checklist

Before submitting this report, complete the following tasks:

- [ ] Replace illustrative prompts with the original prompts where available.
- [ ] Verify that each AI response summary reflects the actual interaction.
- [ ] Add the dates of the relevant interactions.
- [ ] Include relevant user-provided code, requirements, or examples.
- [ ] Document which AI suggestions were implemented, modified, or rejected.
- [ ] Add actual test results instead of unverified expected results.
- [ ] Verify the formal definitions against the implemented models.
- [ ] Include evidence of the four goals in the repository.
- [ ] Add personal reflections based on the work actually completed.
- [ ] Review the report for consistency with the final application.

Final note: This document is a structured report template. The final submission should represent the actual AI interactions and development work performed by the team, rather than treating proposed prompts or expected responses as verified historical evidence.