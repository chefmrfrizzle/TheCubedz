# CANDIDATE-000003 — beginner report

## What did we test?

We tested a known curved-spacetime answer: the empty region outside a spherical, non-rotating mass. The checker calculated how the metric changes from place to place, then checked the connection, curvature, vacuum equations, and a curvature fingerprint.

## What happened?

- Implemented checks passed: **17**
- Implemented checks failed: **0**
- Recorded warnings: **3**
- Overall result: **BENCHMARK_VERIFIED**

The established Schwarzschild exterior metric passed the bound symbolic benchmark under the declared domain and tensor conventions. This calibrates one curved known-answer case; it is not evidence for a novel geometry or transportation mechanism.

## Why begin here?

Before testing an original spacetime idea, the software must correctly recognize a standard curved example with a known answer and clearly mark where its coordinate chart stops working.

## What this does not prove

- The Schwarzschild interior, horizon-penetrating charts, or maximal extension
- Matter-source reconstruction inside the central body
- Geodesic integration, orbit stability, travel time, or tidal-force safety
- Perturbative or nonlinear stability of the spacetime
- Numerical relativity, dynamical collapse, rotation, or charge
- Any novel geometry, device, engineering, or transportation claim
- A passing known-answer benchmark validates bounded software behavior, not the Mars-distance thesis.
- No untrusted symbolic input should be evaluated outside the schema and restricted parser used by this profile.

## Reproducibility fingerprint

`sha256:d2b3f4a2ad15a7ade137e4aaf4166bdefab3ff33a3a2a27e5ca232c5bfb43458`

This fingerprint covers the candidate identity, validator identity, checks, assessment, warnings, errors, and limitations. Runtime metadata such as the clock time is not allowed to change that scientific payload.
