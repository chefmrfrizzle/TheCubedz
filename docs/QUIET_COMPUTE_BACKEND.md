# Quiet Compute validation backend

## Implemented boundary

The repository now implements the deterministic core needed before a public Quiet Compute network can be considered:

- locally sealed measurement artifacts;
- deliberate submission bundles with an explicit artifact allowlist;
- versioned comparison passports;
- matched-workload and matched-environment comparison;
- separate acoustic, thermal, energy, water, reliability, and cost checks;
- Ed25519 verification against an external trust store;
- worker capability and immutable-runtime admission;
- replay, expiry, revocation, quota, and sandbox-attestation checks;
- deterministic diversity-first replication allocation;
- consensus that requires every contract and tolerance to pass;
- evidence-quality reputation with zero weight for money and donated compute; and
- a non-executing, fail-closed isolation plan.

It does not contain a production telemetry collector, upload service, account system, payment system, remote shell, arbitrary-code runner, or public worker executor. It does not prove that an operating data center is quieter. No measurement passport in this repository is preregistered yet.

## Local command surface

Install and recover the existing frozen benchmark first:

```bash
python3.12 scripts/bootstrap.py
```

The installed `research-core` command then exposes local-only Quiet Compute operations:

```text
research-core quiet seal-measurement DRAFT.json --output MEASUREMENT.json
research-core quiet validate-measurement MEASUREMENT.json
research-core quiet seal-passport DRAFT.json --output PASSPORT.json
research-core quiet compare BASELINE.json INTERVENTION.json PASSPORT.json
research-core quiet seal-submission DRAFT.json --output SUBMISSION.json
research-core quiet validate-submission SUBMISSION.json
research-core quiet validate-job ENVELOPE.json TRUST.json WORKER.json
research-core quiet plan-job ENVELOPE.json TRUST.json WORKER.json --replay-ledger LOCAL_NONCES
research-core quiet allocate ENVELOPE.json TRUST.json WORKERS.json PASSPORT.json
research-core quiet consensus SIGNED_RESULTS.json WORKERS.json PASSPORT.json
research-core quiet reputation EVENTS.json
```

There is intentionally no `upload`, `enroll`, `execute`, or `remote-shell` command.

## Algorithms

### Measurement sealing

The canonical digest is SHA-256 over deterministic UTF-8 JSON with sorted keys and compact separators, excluding only the digest field itself. Validation rejects unknown fields, missing sensors, duplicate sensor IDs, unsafe artifact paths, inconsistent measured/missing water or cost values, acoustic values below the declared background, and any digest mismatch.

Every measurement must include acoustic, temperature, and power sensors; calibration identifiers and times; sensor clock offsets; microphone geometry; background level; workload and service target; thermal, energy, water, reliability, and cost observations; raw-artifact digests; provenance; conflict disclosure; and publication terms.

### Deliberate submission

A submission embeds one valid sealed measurement and names only the raw-artifact digests the operator deliberately selected. Its authorization contract requires operator confirmation, automatic upload set to false, credentials included set to false, remote access granted set to false, and a declared terms version. An undeclared artifact digest fails the submission.

### Matched comparison

An intervention can be compared only with the exact baseline it references and the exact passport bound to both artifacts. Exact workload fields are checked independently from numeric workload tolerances. Microphone position and orientation must match; microphone distance, ambient background, and sensor clocks must stay within passport tolerances.

The conservative acoustic improvement is:

```text
(baseline dBA - intervention dBA)
  - confidence_multiplier * hypot(baseline_uncertainty, intervention_uncertainty)
```

It must meet the passport minimum. Clipped audio fails. Thermal, energy, water, reliability, and cost remain separate checks. A failed guardrail cannot be hidden inside an aggregate score.

### Signed job admission

The envelope uses Ed25519. The public key is resolved from a separate trust store; a key supplied only by an untrusted job is never accepted as its own trust anchor. Admission verifies:

1. envelope, manifest, trust-store, and worker schemas;
2. signature over the canonical envelope header, key ID, and manifest bytes;
3. key activity and validity interval;
4. job issue and expiry interval;
5. nonce replay state;
6. worker state and trusted-key allowlist;
7. operation-to-entrypoint binding;
8. immutable runtime digest allowlist;
9. every resource quota; and
10. freshness of the worker's sandbox attestation.

The manifest schema itself requires network denial, rootless execution, a read-only root and inputs, ephemeral scratch, no privileges, no host mounts, and no Linux capabilities.

### Isolation plan

The planner emits fixed argument vectors for three declarative operations only: measurement validation, measurement comparison, and frozen-benchmark reproduction. It carries the immutable image digest, numeric limits, unprivileged user, read-only and no-network requirements, and the external attestation digest.

The planner never launches a process. A production adapter must prove that the operating-system or microVM boundary enforces the plan. This prevents application code from pretending that a JSON flag created real isolation.

### Replication allocation

Every candidate worker first passes the complete signed-job admission algorithm. From eligible workers, the allocator greedily maximizes new values in this order:

1. independence group;
2. operator;
3. operating-system family;
4. hardware family; and
5. sensor stack.

Ties are stable by worker ID. The allocation fails when the passport's minimum result, operator, independence-group, OS, or hardware diversity cannot be met. Repeated machines controlled by one independence group do not become external reproduction by volume.

### Tolerance consensus

Every reproduction must share the exact job, measurement, input digest, and passport. Each envelope is verified with the registered worker's Ed25519 result key. Every provenance record, comparison, and guardrail must pass. The observed spread for each registered metric must be no greater than its declared tolerance.

One out-of-tolerance result produces a mismatch even if every other result agrees. A majority cannot vote away contradictory evidence.

### Evidence-quality reputation

Fixed weights reward verified reproductions, useful negative results, disclosed mismatches, complete provenance, and confirmed adversarial findings. Retractions, false independence, and invalid provenance reduce the score. Unverified events do not count. Funding and donated compute have weight zero.

Reputation helps route review work. It never grants scientific authority and never bypasses a named human promotion decision.

## Security invariants

- No public execution is enabled.
- No job can provide a shell command.
- No mutable tag can replace an approved runtime digest.
- No job can request network access, privileges, capabilities, or host mounts.
- No self-presented public key becomes trusted.
- Expired, future-issued, replayed, revoked, tampered, over-quota, or stale-attestation jobs fail closed.
- No contributor score can be bought with funding or compute volume.
- No consensus result becomes canonical without human review.

## Evidence still required

Before public worker execution, obtain an independent security review of the concrete sandbox adapter, key custody and rotation, replay store, artifact ingestion, decompression limits, host patching, audit logging, incident response, and revocation path. Before a quieter-system claim, obtain an externally reviewed and preregistered passport, physical baseline, intervention, raw traces, and independent reproduction.
