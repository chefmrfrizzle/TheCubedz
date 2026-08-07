# Synthetic benchmark v1: 100 workflow cases

## Purpose

These cases test TheCubedz research instrument. They are not 100 discoveries, 100 physical geometries, or evidence for a transportation claim. A case succeeds when the system returns the preregistered classification, preserves provenance, and refuses to infer more than the implemented check supports.

The suite has four equal blocks. Each case receives a stable ID from `SYN-001` through `SYN-100`, a deterministic fixture, an expected outcome, a rationale, and a failure classification.

## Required result states

- `ACCEPT`: valid input and expected scoped result.
- `REJECT`: invalid or unsafe input rejected with a named reason.
- `MISMATCH`: valid reproduction disagrees with the reference.
- `UNRESOLVED`: the requested conclusion is outside available evidence.
- `NOT_APPLICABLE`: the check is defined but does not apply to the fixture.

No case may silently coerce input, silently repair provenance, or convert `UNRESOLVED` into `PASS`.

## Block A - Schema and representation (`SYN-001` to `SYN-025`)

| ID | Variation | Expected |
|---|---|---|
| 001 | Canonical Candidate 000001 | ACCEPT |
| 002 | JSON object keys reordered | ACCEPT |
| 003 | Insignificant whitespace changed | ACCEPT |
| 004 | Equivalent rational values written with negative denominator | ACCEPT after documented canonicalization |
| 005 | Explicit positive signs represented within allowed schema | ACCEPT |
| 006 | Unknown top-level field | REJECT |
| 007 | Missing candidate identifier | REJECT |
| 008 | Invalid candidate identifier format | REJECT |
| 009 | Unsupported schema version | REJECT |
| 010 | Missing coordinate declaration | REJECT |
| 011 | Duplicate coordinate name | REJECT |
| 012 | Wrong coordinate count | REJECT |
| 013 | Missing metric tensor | REJECT |
| 014 | Metric has three rows | REJECT |
| 015 | Metric has five rows | REJECT |
| 016 | Ragged metric row | REJECT |
| 017 | Non-rational metric entry | REJECT |
| 018 | Zero denominator | REJECT |
| 019 | Boolean supplied where an integer is required | REJECT |
| 020 | Empty assumptions list where policy requires disclosure | REJECT |
| 021 | Unknown validation profile | REJECT |
| 022 | Invalid status vocabulary | REJECT |
| 023 | Duplicate JSON key detected during secure ingestion | REJECT |
| 024 | UTF-8 labels in explanatory metadata | ACCEPT |
| 025 | Executable or script content embedded as a candidate field | REJECT and never execute |

## Block B - Algebra and conventions (`SYN-026` to `SYN-050`)

| ID | Variation | Expected |
|---|---|---|
| 026 | Canonical signature `-+++` | ACCEPT |
| 027 | Declared `+---` metric with matching expected determinant | ACCEPT only under a supported profile |
| 028 | Declared signature disagrees with metric | REJECT |
| 029 | Symmetric off-diagonal pair | ACCEPT if the profile supports it |
| 030 | One unmatched off-diagonal entry | REJECT |
| 031 | Identity inverse for Euclidean test fixture | ACCEPT only under its named non-spacetime profile |
| 032 | Correct Minkowski inverse | ACCEPT |
| 033 | One inverse entry has wrong sign | REJECT |
| 034 | Matrix product differs from identity in one cell | REJECT |
| 035 | Determinant exactly `-1` | ACCEPT |
| 036 | Determinant expectation has wrong sign | REJECT |
| 037 | Singular metric | REJECT |
| 038 | Two timelike directions | UNRESOLVED or REJECT according to declared profile; never call Lorentzian valid |
| 039 | No timelike direction | UNRESOLVED or REJECT according to declared profile |
| 040 | Coordinate labels permuted with tensor transformed consistently | ACCEPT under a supported transform test |
| 041 | Coordinate labels permuted without tensor transform | REJECT |
| 042 | Units declared dimensionless where dimensional parameters are used | REJECT |
| 043 | Natural units declared explicitly | ACCEPT if all quantities are consistent |
| 044 | Mixed incompatible units | REJECT |
| 045 | Domain boundary included as declared | ACCEPT |
| 046 | Evaluation requested outside declared domain | REJECT |
| 047 | Flatness inferred only from constant submitted metric | ACCEPT with scoped wording |
| 048 | General flatness claimed from an unsupported input family | UNRESOLVED |
| 049 | Mathematical pass used to claim stability | UNRESOLVED |
| 050 | Mathematical pass used to claim engineering realizability | UNRESOLVED |

## Block C - Numerical and adversarial behavior (`SYN-051` to `SYN-075`)

These fixtures become executable only when a numerical adapter exists. Until then their correct result is `UNRESOLVED`, not a fabricated pass.

| ID | Variation | Expected |
|---|---|---|
| 051 | Exact value on the tolerance boundary | Preregistered boundary outcome |
| 052 | Exact value one unit inside tolerance | ACCEPT |
| 053 | Exact value one unit outside tolerance | REJECT |
| 054 | Absolute versus relative tolerance conflict | REJECT until policy resolves it |
| 055 | NaN solver output | REJECT |
| 056 | Positive infinity output | REJECT |
| 057 | Negative infinity output | REJECT |
| 058 | Signed zero normalization | ACCEPT with stable canonical form |
| 059 | Catastrophic-cancellation fixture | MISMATCH or flagged instability |
| 060 | Ill-conditioned matrix fixture | UNRESOLVED with conditioning warning |
| 061 | Low-resolution run | UNRESOLVED |
| 062 | Medium-resolution run | UNRESOLVED until convergence sequence completes |
| 063 | Convergent resolution sequence | ACCEPT for convergence only |
| 064 | Divergent resolution sequence | REJECT for convergence |
| 065 | Oscillating resolution sequence | UNRESOLVED |
| 066 | Solver timeout | UNRESOLVED with resource-limit record |
| 067 | Memory quota exceeded | REJECT job; preserve partial logs safely |
| 068 | Output quota exceeded | REJECT job |
| 069 | Nondeterministic output with fixed seed | MISMATCH |
| 070 | Different seed where stochastic behavior is declared | ACCEPT only within preregistered distribution test |
| 071 | Hidden network-call attempt | REJECT and security event |
| 072 | Filesystem traversal attempt | REJECT and security event |
| 073 | Subprocess outside allowlist | REJECT and security event |
| 074 | Dependency mutation during run | REJECT and security event |
| 075 | Result text claims more than numeric payload | REJECT explanation; preserve raw result |

## Block D - Provenance, reproduction, and governance (`SYN-076` to `SYN-100`)

| ID | Variation | Expected |
|---|---|---|
| 076 | Exact clean rerun of the same implementation | ACCEPT as R0 only |
| 077 | Separate environment, same implementation | ACCEPT at declared independence level |
| 078 | Separate implementation, same method | ACCEPT at declared independence level |
| 079 | Separate solver and implementation | ACCEPT at declared independence level |
| 080 | Missing source commit | REJECT reproduction record |
| 081 | Dirty working tree not disclosed | REJECT reproduction record |
| 082 | Missing dependency versions | REJECT reproduction record |
| 083 | Candidate input hash mismatch | MISMATCH |
| 084 | Validator version mismatch | MISMATCH or explicit versioned comparison |
| 085 | Scientific payload digest mismatch | MISMATCH |
| 086 | Presentation-only difference | ACCEPT only if payload digest matches |
| 087 | Missing stdout or stderr record | REJECT complete-passport status |
| 088 | Missing independence declaration | REJECT independent-reproduction claim |
| 089 | Agent approves its own candidate | REJECT authorization |
| 090 | Orchestrator expands its own tool permissions | REJECT authorization |
| 091 | Public user attempts canonical status change | REJECT authorization |
| 092 | Popularity signal attempts physics promotion | REJECT authorization |
| 093 | Explanation changes a source numeric value | REJECT reconciliation |
| 094 | Citation has no source location | REJECT canonical evidence |
| 095 | Generated citation cannot be verified | REJECT canonical evidence |
| 096 | Correction supersedes a result but deletes history | REJECT mutation |
| 097 | Valid correction preserves prior result and link | ACCEPT |
| 098 | Required security review is absent | REJECT promotion |
| 099 | Required reproduction gate is absent | REJECT promotion |
| 100 | All gates pass with signed human decision | ACCEPT promotion record; scientific scope unchanged unless separately approved |

## Execution and reporting contract

1. Freeze suite version, fixtures, expected outcomes, and evaluator commit before a run.
2. Run every case independently with a deterministic seed where applicable.
3. Record expected and observed outcome, reason code, duration, resource use, and artifact hashes.
4. Treat evaluator crashes and missing results as failures.
5. Publish counts by block and outcome; do not publish one universal quality score.
6. Preserve every mismatch and the code version that produced it.
7. Require review for any change to an expected outcome.
8. Keep holdout cases separate before evaluating a learned search or classification policy.

## Conclusions this suite may support

- The workflow accepted and rejected the preregistered cases as expected.
- A particular control failed and requires correction.
- A version improved or regressed on named benchmark dimensions.

It may not support a claim that a novel geometry is physically possible, stable, experimentally supported, or buildable.
