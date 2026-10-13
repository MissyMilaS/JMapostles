# Stage 2 — Qualification Normalization with Finite-State Transducers

## Purpose and interface

This stage receives qualification strings extracted from a resume and maps
known spelling variants to canonical tokens. It does not extract text from a
resume or decide whether the candidate matches a profile; those tasks belong to
Stages 1 and 3.

The implementation is in `src/normalization/fst_normalizer.py`:

- `normalize_qualification(value)` normalizes one qualification, returning
  `None` for an empty value and `UNKNOWN` for a non-empty unsupported value.
- `normalize_sequence(values)` normalizes a sequence, drops empty and unknown
  values, removes duplicate canonical tokens, and preserves first-seen order.

`canonical_sorter.sort_canonical` orders normalized qualifications for a
selected profile after this stage.

## Integration with extraction

`src/pipeline.py` connects Stage 1 to Stage 2 without changing the extraction
module. `process_resume_pipeline(raw_text, profile)` calls
`stage_1_extract_resume_data`, reads its `extracted_skills` list, and adds
`normalized_skills` ordered for the selected profile to the returned candidate
data.

```python
from src.pipeline import process_resume_pipeline

result = process_resume_pipeline(resume_text, profile="FULL_STACK")
print(result["extracted_skills"])
print(result["normalized_skills"])
```

The integration depends on the Stage 1 extractor returning the
`extracted_skills` field. End-to-end tests for `FULL_STACK` and `ML_ENGINEER`
are in `tests/test_pipeline.py`.

## Character-level transducer design

Each canonical qualification has its own `pyformlang.fst.FST`. Unlike a
whole-token edge, each FST consumes the input one character at a time, as in
the class exercise. Input is stripped and case-folded first, so matching is
case-insensitive. Punctuation and spaces are still characters and must match
the alias.

The paths for variants that share a prefix reuse the same states (a trie). For
example, `react` and `react.js` share the path for `r-e-a-c-t`. The output is
emitted only after the input has ended: an epsilon-input transition from each
complete spelling emits the canonical token. This prevents a shorter valid
spelling from emitting output when the input continues as a longer alias.

For a canonical token `c`, let `A_c` be the input spellings in its table row,
including `c` itself, and let `P_c` be all non-empty character prefixes of
those case-folded spellings. The formal 7-tuple is:

`M_c = (Q_c, Σ_c, Γ_c, δ_c, ω_c, q0, F_c)`

- `Q_c = {q0, qf} ∪ {q_p | p ∈ P_c}`: trie states plus the final output state.
- `Σ_c`: the set of characters appearing in `A_c`. The epsilon marker is a
  transition label, not an input character.
- `Γ_c = {c}`: the output alphabet contains the canonical token.
- `δ_c` contains:
  - `(q_p, a, q_pa)` for each trie edge extending prefix `p` with character
    `a`;
  - `(q_w, epsilon, qf)` for each complete input spelling `w ∈ A_c`.
- `ω_c` emits no output on a character edge and emits `c` on a terminal
  epsilon edge. In `pyformlang`, these are output lists `[]` and `[c]`.
- Initial state: `q0`.
- `F_c = {qf}`.

Each spelling has exactly one accepting path in its transducer. For example,
the `REACT` transducer consumes the letters of `react.js`; on the epsilon edge
after the last character it emits `REACT`.

## Transducer families

The canonical token itself is accepted as an input by each transducer.
The table lists the additional aliases, excluding case-only differences.

| Canonical output | Additional accepted input spellings |
|---|---|
| `JAVASCRIPT` | `JS`, `JavaScript` |
| `TYPESCRIPT` | `TS`, `TypeScript` |
| `REACT` | `React.js`, `ReactJS` |
| `NODE_JS` | `Node`, `NodeJS`, `Node.js`, `Node JS` |
| `POSTGRESQL` | `Postgres` |
| `MYSQL` | — |
| `MONGODB` | — |
| `SQLITE` | — |
| `SQL` | — |
| `PYTHON` | — |
| `PANDAS` | — |
| `NUMPY` | — |
| `SCIKIT_LEARN` | `sklearn`, `scikit-learn`, `scikit learn` |
| `TENSORFLOW` | `Tensor Flow` |
| `PYTORCH` | `Py Torch` |
| `GIT` | — |
| `GITHUB` | — |
| `GITHUB_ACTIONS` | `GitHub Actions` |
| `DOCKER` | — |
| `KUBERNETES` | — |
| `AWS` | — |
| `TERRAFORM` | — |
| `JENKINS` | — |
| `SPARK` | — |
| `SNOWFLAKE` | — |
| `AIRFLOW` | — |
| `KAFKA` | — |

`GitHub` has its own `GITHUB` canonical token. It is not mapped to `GIT`
because GitHub is a hosting platform and Git is a version-control system; they
are related but not equivalent qualifications.

## Examples

```text
JS             -> JAVASCRIPT
React.js       -> REACT
NodeJS         -> NODE_JS
Postgres       -> POSTGRESQL
scikit learn   -> SCIKIT_LEARN
Tensor Flow    -> TENSORFLOW
UnknownTech    -> UNKNOWN
```

Normalizing `["Git", "NodeJS", "JS", "Postgres", "React.js"]` produces
`["GIT", "NODE_JS", "JAVASCRIPT", "POSTGRESQL", "REACT"]`. Profile-specific
sorting is a separate operation and produces the order expected by Stage 3.


```mermaid
flowchart LR
    q0((q0)) -->|"j / ε"| q1_js((q1))
    q1_js -->|"s / ε"| q2_js((q2))
    q2_js -->|"ε / JAVASCRIPT"| qf_js(((qf)))
    q2_js -->|"a / ε"| q3_js((q3))
    q3_js -->|"v / ε"| q4_js((q4))
    q4_js -->|"a / ε"| q5_js((q5))
    q5_js -->|"s / ε"| q6_js((q6))
    q6_js -->|"c / ε"| q7_js((q7))
    q7_js -->|"r / ε"| q8_js((q8))
    q8_js -->|"i / ε"| q9_js((q9))
    q9_js -->|"p / ε"| q10_js((q10))
    q10_js -->|"t / ε"| q11_js((q11))
    q11_js -->|"ε / JAVASCRIPT"| qf_js

    q0 -->|"t / ε"| q1_ts((q1))
    q1_ts -->|"s / ε"| q2_ts((q2))
    q2_ts -->|"ε / TYPESCRIPT"| qf_ts(((qf)))
    q1_ts -->|"y / ε"| q3_ts((q3))
    q3_ts -->|"p / ε"| q4_ts((q4))
    q4_ts -->|"e / ε"| q5_ts((q5))
    q5_ts -->|"s / ε"| q6_ts((q6))
    q6_ts -->|"c / ε"| q7_ts((q7))
    q7_ts -->|"r / ε"| q8_ts((q8))
    q8_ts -->|"i / ε"| q9_ts((q9))
    q9_ts -->|"p / ε"| q10_ts((q10))
    q10_ts -->|"t / ε"| q11_ts((q11))
    q11_ts -->|"ε / TYPESCRIPT"| qf_ts

    q0 -->|"r / ε"| q1_re((q1))
    q1_re -->|"e / ε"| q2_re((q2))
    q2_re -->|"a / ε"| q3_re((q3))
    q3_re -->|"c / ε"| q4_re((q4))
    q4_re -->|"t / ε"| q5_re((q5))
    q5_re -->|"ε / REACT"| qf_re(((qf)))
    q5_re -->|"."| q6_re((q6))
    q6_re -->|"j / ε"| q7_re((q7))
    q7_re -->|"s / ε"| q8_re((q8))
    q8_re -->|"ε / REACT"| qf_re
    q5_re -->|"j / ε"| q9_re((q9))
    q9_re -->|"s / ε"| q10_re((q10))
    q10_re -->|"ε / REACT"| qf_re

    q0 -->|"n / ε"| q1_no((q1))
    q1_no -->|"o / ε"| q2_no((q2))
    q2_no -->|"d / ε"| q3_no((q3))
    q3_no -->|"e / ε"| q4_no((q4))
    q4_no -->|"ε / NODE_JS"| qf_no(((qf)))
    q4_no -->|"j / ε"| q5_no((q5))
    q5_no -->|"s / ε"| q6_no((q6))
    q6_no -->|"ε / NODE_JS"| qf_no
    q4_no -->|"."| q7_no((q7))
    q7_no -->|"j / ε"| q8_no((q8))
    q8_no -->|"s / ε"| qf_no
    q4_no -->|"␠ / ε"| q9_no((q9))
    q9_no -->|"j / ε"| q10_no((q10))
    q10_no -->|"s / ε"| qf_no
    q4_no -->|"_"| q11_no((q11))
    q11_no -->|"j / ε"| q12_no((q12))
    q12_no -->|"s / ε"| qf_no

    q0 -->|"p / ε"| q1_pg((q1))
    q1_pg -->|"o / ε"| q2_pg((q2))
    q2_pg -->|"s / ε"| q3_pg((q3))
    q3_pg -->|"t / ε"| q4_pg((q4))
    q4_pg -->|"g / ε"| q5_pg((q5))
    q5_pg -->|"r / ε"| q6_pg((q6))
    q6_pg -->|"e / ε"| q7_pg((q7))
    q7_pg -->|"s / ε"| q8_pg((q8))
    q8_pg -->|"ε / POSTGRESQL"| qf_pg(((qf)))
    q8_pg -->|"q / ε"| q9_pg((q9))
    q9_pg -->|"l / ε"| q10_pg((q10))
    q10_pg -->|"ε / POSTGRESQL"| qf_pg

    q0 -->|"s / ε"| q1_sk((q1))
    q1_sk -->|"k / ε"| q2_sk((q2))
    q2_sk -->|"l / ε"| q3_sk((q3))
    q3_sk -->|"e / ε"| q4_sk((q4))
    q4_sk -->|"a / ε"| q5_sk((q5))
    q5_sk -->|"r / ε"| q6_sk((q6))
    q6_sk -->|"n / ε"| q7_sk((q7))
    q7_sk -->|"ε / SCIKIT_LEARN"| qf_sk(((qf)))
    q1_sk -->|"c / ε"| q8_sk((q8))
    q8_sk -->|"i / ε"| q9_sk((q9))
    q9_sk -->|"k / ε"| q10_sk((q10))
    q10_sk -->|"_"| q11_sk((q11))
    q10_sk -->|"-"| q12_sk((q12))
    q10_sk -->|"␠ / ε"| q13_sk((q13))
    q11_sk -->|"l / ε"| q14_sk((q14))
    q12_sk -->|"l / ε"| q14_sk
    q13_sk -->|"l / ε"| q14_sk
    q14_sk -->|"e / ε"| q15_sk((q15))
    q15_sk -->|"a / ε"| q16_sk((q16))
    q16_sk -->|"r / ε"| q17_sk((q17))
    q17_sk -->|"n / ε"| q18_sk((q18))
    q18_sk -->|"ε / SCIKIT_LEARN"| qf_sk

    q0 -->|"t / ε"| q1_tf((q1))
    q1_tf -->|"e / ε"| q2_tf((q2))
    q2_tf -->|"n / ε"| q3_tf((q3))
    q3_tf -->|"s / ε"| q4_tf((q4))
    q4_tf -->|"o / ε"| q5_tf((q5))
    q5_tf -->|"r / ε"| q6_tf((q6))
    q6_tf -->|"f / ε"| q7_tf((q7))
    q6_tf -->|"␠ / ε"| q8_tf((q8))
    q8_tf -->|"f / ε"| q7_tf
    q7_tf -->|"l / ε"| q9_tf((q9))
    q9_tf -->|"o / ε"| q10_tf((q10))
    q10_tf -->|"w / ε"| q11_tf((q11))
    q11_tf -->|"ε / TENSORFLOW"| qf_tf(((qf)))

    q0 -->|"p / ε"| q1_pt((q1))
    q1_pt -->|"y / ε"| q2_pt((q2))
    q2_pt -->|"t / ε"| q3_pt((q3))
    q2_pt -->|"␠ / ε"| q4_pt((q4))
    q4_pt -->|"t / ε"| q3_pt
    q3_pt -->|"o / ε"| q5_pt((q5))
    q5_pt -->|"r / ε"| q6_pt((q6))
    q6_pt -->|"c / ε"| q7_pt((q7))
    q7_pt -->|"h / ε"| q8_pt((q8))
    q8_pt -->|"ε / PYTORCH"| qf_pt(((qf)))

    q0 -->|"g / ε"| q1_gh((q1))
    q1_gh -->|"i / ε"| q2_gh((q2))
    q2_gh -->|"t / ε"| q3_gh((q3))
    q3_gh -->|"h / ε"| q4_gh((q4))
    q4_gh -->|"u / ε"| q5_gh((q5))
    q5_gh -->|"b / ε"| q6_gh((q6))
    q6_gh -->|"_"| q7_gh((q7))
    q6_gh -->|"␠ / ε"| q8_gh((q8))
    q7_gh -->|"a / ε"| q9_gh((q9))
    q8_gh -->|"a / ε"| q9_gh
    q9_gh -->|"c / ε"| q10_gh((q10))
    q10_gh -->|"t / ε"| q11_gh((q11))
    q11_gh -->|"i / ε"| q12_gh((q12))
    q12_gh -->|"o / ε"| q13_gh((q13))
    q13_gh -->|"n / ε"| q14_gh((q14))
    q14_gh -->|"s / ε"| q15_gh((q15))
    q15_gh -->|"ε / GITHUB_ACTIONS"| qf_gh(((qf)))

