# CANDIDATE-000002 — technical report

## Candidate

- Title: **Minkowski spacetime in rescaled inertial coordinates**
- Candidate version: `1.0.0`
- Candidate SHA-256: `d80416efff1f74a63104f4f56d003b9b2e844f34976893349645726917351bd4`
- Validation profile: `benchmark.minkowski_linear_rescaled_v1`
- Validator: `deterministic-baseline-validator@0.2.1`
- Scientific payload: `sha256:73af7803b5ae10a9f8b1269398a126e6da94072b30a7e12da16f3e8f53e012d2`
- Benchmark passport: `PASSPORT-000002@1.0.1`
- Validation-contract digest: `sha256:e79125b196019405e244106ecb5000087f37b18910a36c1fcd389bd45958ae76`

## Conventions

- Coordinates: `tau, xi, eta, zeta`
- Signature: `-+++`
- Units: `dimensionless rescaled geometrized natural units`
- Speed of light: `1`
- Cosmological constant: `0`

## Implemented checks

| Check | Status | Result | Method |
|---|---|---|---|
| `schema.candidate.v1` | PASS | Candidate matches the versioned candidate schema. | JSON Schema Draft 2020-12 validation |
| `metric.dimension` | PASS | Metric dimensions agree with the declared coordinate count. | Exact matrix shape comparison |
| `metric.symmetry` | PASS | Metric components are symmetric. | Exact component comparison g[i,j] = g[j,i] |
| `metric.determinant` | PASS | Metric determinant exactly matches the benchmark passport. | Exact fraction-preserving Gaussian elimination and passport comparison |
| `metric.inverse` | PASS | Metric inverse exactly matches the benchmark passport. | Exact Gauss-Jordan inversion and passport comparison |
| `coordinate_map.coordinates` | PASS | Coordinate-map labels match both benchmark charts. | Exact ordered coordinate-list comparison |
| `coordinate_map.jacobian` | PASS | The complete Jacobian exactly matches the versioned benchmark passport and is invertible. | Exact component and determinant comparison against the benchmark passport |
| `coordinate_map.pullback` | PASS | The submitted metric and exact pullback both match the benchmark passport. | Exact matrix multiplication and component comparison against the benchmark passport |
| `minkowski.signature` | PASS | Declared signature matches the benchmark profile. | Declared convention comparison |
| `minkowski.cosmological_constant` | PASS | Cosmological constant is zero for this benchmark. | Declared convention comparison |
| `minkowski.constant_components` | PASS | Metric and Jacobian entries are supported exact constants. | Schema-limited inspection of numeric literals |
| `minkowski.connection` | PASS | Christoffel symbols vanish in the declared rescaled inertial coordinates. | Analytic implication from constant metric components |
| `minkowski.curvature` | PASS | Riemann, Ricci, scalar curvature, and Einstein tensors vanish for this profile. | Analytic implication from the vanishing connection and its derivatives |
| `minkowski.vacuum_source` | PASS | The profile is consistent with zero stress-energy under a zero cosmological constant. | Einstein field equation implication for a vanishing Einstein tensor and cosmological constant |

## Assessment

- Overall: `BENCHMARK_VERIFIED`
- Mathematics: `PASSED_IMPLEMENTED_LINEAR_COORDINATE_BENCHMARK_CHECKS`
- Physical scope: `VACUUM_BASELINE_ONLY`
- Transportation scope: `NOT_A_TRANSPORTATION_PROPOSAL`

The submitted rescaled-coordinate metric exactly matches the declared linear pullback of the canonical Minkowski metric. This verifies one bounded coordinate-equivalence capability, not a general coordinate solver or transportation capability.

## Warnings

- Coordinate equivalence is established only for the exact declared constant linear map; nonlinear and inferred transformations remain unsupported.

## Errors

- None

## Limitations

- The implementation validates one preregistered constant linear coordinate map, not arbitrary coordinate transformations.
- It does not support position-dependent metric components or symbolic tensor calculus.
- It does not solve Einstein's equations for general candidate metrics.
- It does not evaluate geodesics, travel time, energy conditions, stability, causality, traveler safety, or engineering realizability.
- A passing result shows the same established flat geometry in two representations; it is not a novel-physics result or transportation evidence.
