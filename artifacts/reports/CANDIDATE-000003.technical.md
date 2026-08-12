# CANDIDATE-000003 — technical report

## Candidate

- Title: **Schwarzschild exterior in curvature coordinates**
- Candidate version: `1.0.0`
- Candidate SHA-256: `0437c86a532e8d87976f7e4c5e7e4598f0cd9762e2908307e42db48fa1d437bc`
- Validation profile: `benchmark.schwarzschild_exterior_v1`
- Validator: `symbolic-curved-benchmark-validator@0.1.0`
- Scientific payload: `sha256:d2b3f4a2ad15a7ade137e4aaf4166bdefab3ff33a3a2a27e5ca232c5bfb43458`
- Benchmark passport: `PASSPORT-000003@1.0.0`
- Validation-contract digest: `sha256:d8f983d51a22fbb9dd36912da31d5593843c4e9cdb5f45fdbeb6309e1df01e21`

## Conventions

- Coordinates: `t, r, theta, phi`
- Signature: `-+++`
- Units: `geometrized units G = c = 1`
- Speed of light: `1`
- Cosmological constant: `0`

## Implemented checks

| Check | Status | Result | Method |
|---|---|---|---|
| `schema.candidate.v2` | PASS | Candidate matches the curved-benchmark schema. | JSON Schema Draft 2020-12 validation |
| `schema.passport.curved.v1` | PASS | Passport matches the curved-benchmark passport schema. | JSON Schema Draft 2020-12 validation |
| `metric.dimension` | PASS | Metric has one row and column per coordinate. | Exact matrix shape comparison |
| `metric.symmetry` | PASS | Metric is symmetric. | Exact symbolic component comparison |
| `metric.components` | PASS | Every metric component matches the preregistered Schwarzschild exterior metric. | Exact symbolic equality after simplification |
| `metric.determinant` | PASS | Metric determinant matches the passport. | Symbolic determinant and exact simplification |
| `metric.inverse` | PASS | Inverse metric matches the passport. | Symbolic matrix inversion and exact component comparison |
| `domain.schwarzschild_exterior` | PASS | Mass, exterior-radius, angular, horizon, and singularity restrictions match the passport. | Exact structured declaration comparison |
| `symbolic.position_dependence` | PASS | The metric has verified radial and angular position dependence. | Symbolic partial differentiation |
| `connection.christoffel` | PASS | The complete nonzero Christoffel set matches the passport. | Levi-Civita connection from symbolic first derivatives |
| `curvature.riemann_nonzero` | PASS | Curvature is nonzero and every preregistered representative Riemann component matches. | Declared Riemann convention from Christoffel derivatives and products |
| `curvature.ricci_zero` | PASS | Every Ricci-tensor component vanishes. | Full contraction R^rho_{sigma rho nu} |
| `curvature.ricci_scalar_zero` | PASS | Ricci scalar is zero. | Exact contraction g^mu_nu R_mu_nu |
| `curvature.einstein_zero` | PASS | Every Einstein-tensor component vanishes. | G_mu_nu = R_mu_nu - (1/2) g_mu_nu R |
| `curvature.kretschmann` | PASS | Kretschmann scalar matches the established radial curvature invariant. | Exact contraction R_abcd R^abcd for the preregistered diagonal metric |
| `conventions.tensor_signs` | PASS | Signature, Riemann sign, Ricci contraction, units, and cosmological constant match the passport. | Exact declaration comparison |
| `physics.vacuum_exterior` | PASS | The chart satisfies the classical vacuum field equations for Lambda = 0. | Einstein equation implication from G_mu_nu = 0 and Lambda = 0 |

## Assessment

- Overall: `BENCHMARK_VERIFIED`
- Mathematics: `PASSED_PREREGISTERED_CURVED_BENCHMARK_CHECKS`
- Physical scope: `CURVED_VACUUM_EXTERIOR_BENCHMARK_ONLY`
- Transportation scope: `NOT_A_TRANSPORTATION_PROPOSAL`

The established Schwarzschild exterior metric passed the bound symbolic benchmark under the declared domain and tensor conventions. This calibrates one curved known-answer case; it is not evidence for a novel geometry or transportation mechanism.

## Warnings

- Schwarzschild curvature coordinates do not cover the horizon or interior; r = 2M is excluded from this chart.
- Coordinate components and signs are convention-sensitive; comparisons use only the declared Riemann and Ricci conventions.
- The primary calculation and separate solver comparison are project-internal checks, not independent scientific review.

## Errors

- None

## Limitations

- The Schwarzschild interior, horizon-penetrating charts, or maximal extension
- Matter-source reconstruction inside the central body
- Geodesic integration, orbit stability, travel time, or tidal-force safety
- Perturbative or nonlinear stability of the spacetime
- Numerical relativity, dynamical collapse, rotation, or charge
- Any novel geometry, device, engineering, or transportation claim
- A passing known-answer benchmark validates bounded software behavior, not the Mars-distance thesis.
- No untrusted symbolic input should be evaluated outside the schema and restricted parser used by this profile.
