# Quiet Compute build program

These prompts are ordered. Run one bounded stage at a time. A later stage may not upgrade the status of an earlier stage without its named evidence.

Implementation note: Prompts 1-3 and the deterministic portions of Prompts 5-7 now have repository contracts and adversarial tests. Prompt 4 still requires physical measurements. Prompt 6 still requires outside operators. Public job execution remains disabled pending an independent sandbox review.

## Shared boundary for every prompt

The public campaign line is **"Data centers are too freaking loud."** The response is **"Let's make them quiet."** The scientific question is narrower: can a declared compute system reduce acoustic output under the same useful workload while satisfying thermal, energy, water, reliability, cost, uncertainty, and independent-reproduction constraints?

Do not assume superconductivity is the answer. Do not present simulation as measurement. Do not claim NVIDIA partnership, material discovery, or a quieter system without a reviewed artifact. Preserve negative results and conflicts of interest.

## Prompt 1 - Scope the first test

```text
Act as the Quiet Compute benchmark designer. Define the smallest useful V0 system boundary: one declared server or rack, one repeatable workload, one documented cooling path, and one acoustic/thermal environment. Specify inputs, units, sensor placement, warm-up, steady-state window, ambient correction, repeated-run design, raw trace format, uncertainty, exclusions, and falsification conditions. Separate required fields from optional fields. Return a draft contract only; do not invent measurements or mark the benchmark preregistered.
```

## Prompt 2 - Design the measurement schema

```text
Act as a measurement-data architect. Convert the reviewed Quiet Compute V0 contract into versioned JSON Schemas for system, workload, acoustic trace, thermal trace, energy trace, water trace, intervention, result, and reproduction records. Require units, calibration state, timestamps, equipment identity, geometry, operating state, missing-data reasons, uncertainty, provenance, and digests. Add valid fixtures and adversarial invalid fixtures. Reject silent field coercion and unknown fields. Do not add a scientific conclusion field that can bypass deterministic evaluation.
```

## Prompt 3 - Build Round 0 calibration

```text
Act as the calibration engineer. Design known-positive, known-negative, and adversarial cases for the Quiet Compute measurement pipeline before evaluating a real intervention. Include at least: calibrated reference sound, ambient-background contamination, microphone-position mismatch, workload mismatch, fan-off thermal failure, throttled-workload false improvement, missing facility-boundary source, sensor clock drift, clipped audio, and inconsistent units. Define deterministic checks and exact expected outcomes. Do not use a synthetic pass as evidence of a quieter data center.
```

## Prompt 4 - Establish one baseline

```text
Act as the baseline operator. Using only the frozen V0 passport and declared equipment, run the prescribed repeated measurements. Record operating system, firmware, hardware, workload, commands, sensor calibration, positions, ambient conditions, raw traces, exclusions, uncertainty, and digests. Report every deviation. Produce a signed baseline artifact with status MEASURED_UNREVIEWED. Do not optimize or change the workload during baseline collection.
```

## Prompt 5 - Compare one intervention

```text
Act as the intervention evaluator. Compare exactly one declared control, airflow, liquid-cooling, power, or thermal-material change against the frozen baseline. Randomize run order where practical, match useful workload, and evaluate acoustic level and spectrum plus all thermal, energy, water, reliability, cost, and uncertainty guardrails. Fail the candidate if any required guardrail fails or is unmeasured. Return separate metric outcomes; do not compress them into one score.
```

## Prompt 6 - Reproduce and attack the result

```text
Act as an independent reproducer and skeptic. Re-run the frozen baseline and intervention using a separate operator, environment, and preferably separate measurement or analysis implementation. Search for workload changes, shifted heat, excluded sound sources, ambient leakage, sensor-placement effects, multiple-comparison bias, cherry-picked windows, hidden maintenance state, and cost externalization. Record conflicts of interest and every disagreement. Agreement may support reproduction; it does not create general validity.
```

## Prompt 7 - Build the secure compute worker

```text
Act as the distributed-compute security engineer. Implement only signed declarative work manifests for reviewed Quiet Compute simulations and parameter sweeps. The worker must be rootless, read inputs read-only, deny network during compute, enforce CPU/GPU/memory/disk/time quotas, expose pause/remove controls, use ephemeral scratch space, produce signed provenance, and never execute arbitrary public shell commands. Add threat-model tests for malicious manifests, path escape, decompression bombs, resource exhaustion, replay, result forgery, dependency substitution, signing-key compromise, and colluding workers. Public enrollment remains disabled until an independent security review approves it.
```

## Prompt 8 - Operate the evidence network responsibly

```text
Act as the evidence-network operator. Publish contributor terms, data and commercial-use rights, privacy boundaries, security contacts, incident response, signing-key rotation, revocation, dispute handling, and human-promotion rules before accepting public measurements or compute. Keep scientific status independent from payments, hardware volume, and reputation. Report network health and failures without exposing contributor secrets. Do not enable public execution until the concrete sandbox, artifact ingestion, replay store, and key custody pass independent review.
```

## Stop conditions

- Stop materials search if no experimental or hardware partner can validate candidates.
- Stop distributed public execution if the worker security review is incomplete.
- Stop a quieter-system claim if the workload differs or any required guardrail is missing.
- Stop a superconductivity claim without zero-resistance and magnetic evidence under declared pressure, temperature, field, and current conditions.
- Stop contribution intake when data rights, commercial-use terms, privacy, or withdrawal rules are ambiguous.
