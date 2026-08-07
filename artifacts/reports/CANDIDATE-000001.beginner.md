# CANDIDATE-000001 — beginner report

## What did we test?

We tested the project's first baseline: ordinary flat spacetime, written as a four-by-four matrix. This candidate is the empty test track for the research system. It is not a shortcut to Mars.

## What happened?

- Implemented checks passed: **12**
- Implemented checks failed: **0**
- Recorded warnings: **1**
- Overall result: **BASELINE_VERIFIED**

The exact submitted Minkowski Cartesian benchmark passed every implemented V0 check. This verifies the baseline pipeline, not a general relativity solver or transportation capability.

## Why begin here?

Before a search system examines unusual ideas, it must show that it can represent, hash, check, explain, and reproduce a simple known baseline without changing the result.

## What this does not prove

- The implementation validates one exact constant-component Minkowski benchmark profile.
- It does not perform arbitrary coordinate transformations or symbolic tensor calculus.
- It does not solve Einstein's equations for general candidate metrics.
- It does not evaluate energy conditions, stability, causality, geodesics, or engineering realizability for exotic candidates.
- A passing result is a software/reproducibility milestone, not evidence for spacetime transportation.

## Reproducibility fingerprint

`sha256:91b67470ddfade1770e76793fef54d2f3812ad41f726bda16a3246fb2b428b4b`

This fingerprint covers the candidate identity, validator identity, checks, assessment, warnings, errors, and limitations. Runtime metadata such as the clock time is not allowed to change that scientific payload.
