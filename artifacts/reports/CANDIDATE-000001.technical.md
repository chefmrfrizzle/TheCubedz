# CANDIDATE-000001 — technical report

## Candidate

- Title: **Minkowski spacetime baseline in Cartesian coordinates**
- Candidate version: `1.0.0`
- Candidate SHA-256: `0e9c36562cb650f3d9eb96efb6c9e1daceb8d284a4a8c5b457722d8f9c25e4c8`
- Validation profile: `benchmark.minkowski_cartesian_v1`
- Validator: `deterministic-baseline-validator@0.2.0`
- Scientific payload: `sha256:91b67470ddfade1770e76793fef54d2f3812ad41f726bda16a3246fb2b428b4b`

## Conventions

- Coordinates: `t, x, y, z`
- Signature: `-+++`
- Units: `geometrized natural units`
- Speed of light: `1`
- Cosmological constant: `0`

## Implemented checks

| Check | Status | Result | Method |
|---|---|---|---|
| `schema.candidate.v1` | PASS | Candidate matches the versioned candidate schema. | JSON Schema Draft 2020-12 validation |
| `metric.dimension` | PASS | Metric dimensions agree with the declared coordinate count. | Exact matrix shape comparison |
| `metric.symmetry` | PASS | Metric components are symmetric. | Exact component comparison g[i,j] = g[j,i] |
| `metric.determinant` | PASS | Metric is non-degenerate. | Exact fraction-preserving Gaussian elimination |
| `metric.inverse` | PASS | An exact inverse exists for the submitted matrix. | Gauss-Jordan elimination using rational arithmetic |
| `minkowski.components` | PASS | Components match the declared Minkowski Cartesian baseline. | Exact matrix equality under the selected validation profile |
| `minkowski.signature` | PASS | Declared signature matches the baseline profile. | Declared convention comparison |
| `minkowski.cosmological_constant` | PASS | Cosmological constant is zero for this baseline. | Declared convention comparison |
| `minkowski.constant_components` | PASS | All submitted components are coordinate-independent constants. | Schema-limited inspection of numeric component literals |
| `minkowski.connection` | PASS | Christoffel symbols vanish in the declared Cartesian inertial coordinates. | Analytic implication: derivatives of constant metric components are zero. |
| `minkowski.curvature` | PASS | Riemann, Ricci, scalar curvature, and Einstein tensors vanish for this profile. | Analytic implication from the vanishing connection and its derivatives. |
| `minkowski.vacuum_source` | PASS | The profile is consistent with a zero stress-energy tensor under Λ = 0. | Einstein field equation implication for Gμν = 0 and Λ = 0. |

## Assessment

- Overall: `BASELINE_VERIFIED`
- Mathematics: `PASSED_IMPLEMENTED_MINKOWSKI_BASELINE_CHECKS`
- Physical scope: `VACUUM_BASELINE_ONLY`
- Transportation scope: `NOT_A_TRANSPORTATION_PROPOSAL`

The exact submitted Minkowski Cartesian benchmark passed every implemented V0 check. This verifies the baseline pipeline, not a general relativity solver or transportation capability.

## Warnings

- The validator recognizes one exact benchmark representation; it does not prove equivalence under arbitrary coordinate transformations.

## Errors

- None

## Limitations

- The implementation validates one exact constant-component Minkowski benchmark profile.
- It does not perform arbitrary coordinate transformations or symbolic tensor calculus.
- It does not solve Einstein's equations for general candidate metrics.
- It does not evaluate energy conditions, stability, causality, geodesics, or engineering realizability for exotic candidates.
- A passing result is a software/reproducibility milestone, not evidence for spacetime transportation.
