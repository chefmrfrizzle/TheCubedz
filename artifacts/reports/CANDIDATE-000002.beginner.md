# CANDIDATE-000002 — beginner report

## What did we test?

We tested whether a differently numbered coordinate grid still describes the same ordinary flat spacetime. The checker used the declared conversion table to transform the original metric and compared every number exactly.

## What happened?

- Implemented checks passed: **14**
- Implemented checks failed: **0**
- Recorded warnings: **1**
- Overall result: **BENCHMARK_VERIFIED**

The submitted rescaled-coordinate metric exactly matches the declared linear pullback of the canonical Minkowski metric. This verifies one bounded coordinate-equivalence capability, not a general coordinate solver or transportation capability.

## Why begin here?

A trustworthy geometry checker must distinguish a real physical difference from a harmless change in coordinate labels or scales.

## What this does not prove

- The implementation validates one preregistered constant linear coordinate map, not arbitrary coordinate transformations.
- It does not support position-dependent metric components or symbolic tensor calculus.
- It does not solve Einstein's equations for general candidate metrics.
- It does not evaluate geodesics, travel time, energy conditions, stability, causality, traveler safety, or engineering realizability.
- A passing result shows the same established flat geometry in two representations; it is not a novel-physics result or transportation evidence.

## Reproducibility fingerprint

`sha256:73af7803b5ae10a9f8b1269398a126e6da94072b30a7e12da16f3e8f53e012d2`

This fingerprint covers the candidate identity, validator identity, checks, assessment, warnings, errors, and limitations. Runtime metadata such as the clock time is not allowed to change that scientific payload.
