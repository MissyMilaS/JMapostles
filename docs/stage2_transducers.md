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
