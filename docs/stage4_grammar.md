# Stage 4: Candidate Profile DSL and Visualization

## Objective

Stage 4 represents and validates the structured candidate data produced by
ResumeLens. It does not extract résumé text, normalize qualifications, or
classify candidates. Instead, it takes those prior-stage results, serializes
them in a domain-specific language (DSL), validates the representation with
textX, and generates a human-readable HTML report from the parsed model.

```text
Résumé text
    -> extraction
    -> qualification normalization
    -> profile classification
    -> candidate DSL serialization and validation
    -> HTML visualization
```

## Language structure

The language describes one candidate. A candidate has a name, contact
information, normalized skills, and classification results. Work experience is
optional and can contain multiple role/year records.

### Terminals

Terminals are the literal keywords and punctuation used by the DSL:

- Keywords: `candidate`, `contact`, `email`, `phone`, `experience`, `role`,
  `years`, `skills`, `classification`
- Profile identifiers: `FULL_STACK_DEVELOPER`,
  `MACHINE_LEARNING_ENGINEER`, `SOFTWARE_ENGINEER`, `DATA_ENGINEER`
- Status identifiers: `ACCEPTED`, `REJECTED`
- Delimiters: `{`, `}`, `:`, `,`
- textX built-in tokens: `STRING` for quoted text, `ID` for skill identifiers,
  and `INT` for integer years

### Non-terminals

The grammar's non-terminals are `Resume`, `ContactDetails`,
`ExperienceSection`, `ExperienceEntry`, `SkillsSection`,
`ClassificationSection`, `ProfileEvaluation`, `ProfileName`, and `Status`.

## EBNF specification

```ebnf
Resume                 ::= "candidate" STRING "{"
                           ContactDetails
                           [ ExperienceSection ]
                           SkillsSection
                           ClassificationSection
                           "}"

ContactDetails         ::= "contact" "{"
                           "email" ":" STRING
                           "phone" ":" STRING
                           "}"

ExperienceSection      ::= "experience" "{"
                           ExperienceEntry { ExperienceEntry }
                           "}"

ExperienceEntry        ::= "role" ":" STRING "years" ":" INT

SkillsSection          ::= "skills" "{"
                           ID { "," ID }
                           "}"

ClassificationSection  ::= "classification" "{"
                           ProfileEvaluation { ProfileEvaluation }
                           "}"

ProfileEvaluation      ::= ProfileName ":" Status

ProfileName            ::= "FULL_STACK_DEVELOPER"
                         | "MACHINE_LEARNING_ENGINEER"
                         | "SOFTWARE_ENGINEER"
                         | "DATA_ENGINEER"

Status                 ::= "ACCEPTED" | "REJECTED"
```

In this EBNF, square brackets mean optional, braces mean repetition, and
vertical bars mean alternatives. The textX implementation requires at least
one entry in each present repeated section; semantic validation further
requires at least one skill and exactly one classification result for each
supported profile.

## Structural and validation rules

- Candidate name, contact, skills, and classification are mandatory.
- The experience section is optional. When supplied, it contains one or more
  role/year entries.
- Contact email and phone are quoted strings; semantic validation checks their
  formats.
- Skills are comma-separated identifiers. Each must be a unique, uppercase
  normalized token (for example `NODE_JS` or `SCIKIT_LEARN`).
- Classification entries use only the four declared profile names and the
  statuses `ACCEPTED` or `REJECTED`. Every supported profile must appear once.
- Candidate name and experience role cannot be blank; experience years cannot
  be negative.
- textX rejects malformed strings, unknown keywords or enum values, missing
  delimiters, and invalid list separators as syntax errors. Semantic violations
  are rejected after parsing.

## textX grammar

The executable grammar is [candidate_dsl.tx](../src/dsl/candidate_dsl.tx):

```textx
Resume:
    'candidate' name=STRING '{'
        contact=ContactDetails
        experience=ExperienceSection?
        skills=SkillsSection
        classifications=ClassificationSection
    '}';

ContactDetails:
    'contact' '{'
        'email' ':' email=STRING
        'phone' ':' phone=STRING
    '}';

ExperienceSection:
    'experience' '{'
        entries+=ExperienceEntry
    '}';

ExperienceEntry:
    'role' ':' role=STRING 'years' ':' years=INT
;

SkillsSection:
    'skills' '{'
        skills+=ID[',']
    '}';

ClassificationSection:
    'classification' '{'
        evaluations+=ProfileEvaluation
    '}';

ProfileEvaluation:
    profile=ProfileName ':' status=Status
;

ProfileName:
    'FULL_STACK_DEVELOPER'
    | 'MACHINE_LEARNING_ENGINEER'
    | 'SOFTWARE_ENGINEER'
    | 'DATA_ENGINEER'
;

Status:
    'ACCEPTED' | 'REJECTED'
;
```

The parser and semantic checks are implemented in
[validator.py](../src/dsl/validator.py). The serializer that converts pipeline
results into this syntax and writes the specification is in
[specification.py](../src/dsl/specification.py). Internal classifier names map
to DSL identifiers as follows: `FULL_STACK` to `FULL_STACK_DEVELOPER`,
`ML_ENGINEER` to `MACHINE_LEARNING_ENGINEER`, and `DEVOPS_ENGINEER` to
`SOFTWARE_ENGINEER`; `DATA_ENGINEER` keeps its name.

## Example candidate specification

```text
candidate "Wednesday Addams" {
    contact {
        email: "wednesday@nevermore.edu"
        phone: "+1-555-0192"
    }
    experience {
        role: "Web Developer" years: 3
        role: "Backend Developer" years: 2
    }
    skills {
        JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT
    }
    classification {
        FULL_STACK_DEVELOPER: ACCEPTED
        MACHINE_LEARNING_ENGINEER: REJECTED
        SOFTWARE_ENGINEER: REJECTED
        DATA_ENGINEER: REJECTED
    }
}
```

The `experience` block may be omitted for candidates without experience. It
must contain at least one entry if present.

## Visualization and application flow

After successful parsing and semantic validation,
[visualizer.py](../src/dsl/visualizer.py) renders the candidate as an HTML
report. The report includes contact details, an experience table, normalized
skill tags, and classification statuses. HTML text values are escaped before
rendering.

[specification.py](../src/dsl/specification.py) writes the validated DSL
specification (`.resume`) and HTML report (`.html`) to the requested output
directory. The Streamlit interface in [main.py](../main.py) runs the pipeline,
shows the classification results, and offers the DSL and HTML report for
download after successful validation.

## Validation scenarios

Automated cases are in [test_stage4.py](../tests/test_stage4.py). They verify:

1. A valid candidate with multiple experience records parses and preserves its
   repeated skills and profile results.
2. A candidate without an experience section is accepted.
3. Missing commas between skills are rejected as syntax errors.
4. An unsupported profile identifier is rejected as a syntax error.
5. An invalid email and incomplete profile classifications are rejected as
   semantic errors.
6. Structured output from the candidate pipeline can be serialized, validated,
   and written as both a `.resume` specification and HTML report.
