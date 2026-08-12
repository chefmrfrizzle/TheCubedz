# Quiet Compute participation and network logic

## Current truth

The public repository now provides local measurement, passport, deliberate-submission, comparison, signed-job admission, worker eligibility, diversity allocation, tolerance consensus, reputation, benchmark, schema, and website tooling. It does **not** provide a public distributed-compute executor, production scheduler service, data-center telemetry agent, remote administration service, or paid marketplace.

The install command on the website clones the public repository, creates a repository-local Python environment, installs declared Python and Node.js dependencies, and runs a local synthetic smoke test. It does not enroll the machine or transmit a result.

## Participant journey

1. **Discover** — understand the Quiet Compute question and claim boundaries.
2. **Install locally** — clone the exact public repository and create `.venv`.
3. **Self-test** — recover a frozen synthetic benchmark before creating new evidence.
4. **Review terms** — inspect the code, license, measurement contract, privacy boundary, and intended artifact before sharing anything.
5. **Declare one system** — describe hardware, workload, cooling path, sensors, environment, and allowed disclosure.
6. **Measure a baseline** — record calibrated sound, spectrum, workload, temperature, energy, and applicable water data locally.
7. **Create an artifact** — remove unrelated private data, attach uncertainty and provenance, and compute a digest.
8. **Submit deliberately** — the operator chooses what to upload; there is no automatic production telemetry.
9. **Validate and reproduce** — deterministic checks reject malformed or mismatched records, and a separate operator repeats accepted work.
10. **Promote by human review** — no algorithm, contributor, agent, payment, or compute donation can promote a canonical claim alone.

## Implemented evidence algorithms

### 1. Measurement and submission validator

Reject a record unless required sensor calibration, clocks, microphone geometry, background level, workload, temperatures, equipment identity, uncertainty, provenance, conflict disclosure, publication terms, and raw-artifact digests are present and schema-valid. A separate deliberate-submission bundle allows only operator-selected artifact digests and forbids automatic upload, credentials, and remote access.

### 2. Matched-workload comparator

Compare a proposed intervention with its frozen baseline only when the useful-workload and service targets match within preregistered tolerances. Return separate acoustic, thermal, energy, water, reliability, and cost outcomes. Never compress a failed guardrail into a passing aggregate score.

### 3. Signed task eligibility filter

A worker profile may accept a plan only when its Ed25519 signature chains to a separately configured trust store, the nonce is fresh, the immutable runtime and fixed entrypoint are approved, the requested operation is supported, every quota fits, and the manifest forbids network, host mounts, privilege, capabilities, and writable inputs. The library emits a plan but cannot execute it.

### 4. Replication allocator

Assign the same frozen work unit to unrelated eligible environments. Prefer diversity of operator, operating system, hardware, sensor stack, and solver. Do not treat repeated runs controlled by one owner as external reproduction.

### 5. Result-consensus engine

Group results by exact input and environment declarations. Compare scientific payloads and tolerances, preserve disagreements, and route mismatches to review. Majority agreement cannot overrule a broken contract or missing evidence.

### 6. Evidence-quality reputation

Reputation should reward reproducibility, complete provenance, useful negative results, accurate uncertainty, and successful adversarial review. It must not be purchasable or determined only by donated compute volume.

Full details and command examples are in [Quiet Compute validation backend](QUIET_COMPUTE_BACKEND.md).

## Safe development phases

### Phase A — local tools and manual artifacts

- Public now.
- No accounts, remote jobs, telemetry, or automatic uploads.
- The validation core is implemented as a draft. External domain review, preregistration, and the first physical baseline remain open.

### Phase B — signed local worker prototype

- Declarative operations only.
- Rootless isolation, read-only inputs, ephemeral scratch space, no network during compute, and explicit resource limits.
- A visible pause/remove control and a preview of every outbound artifact.
- Admission and isolation-plan generation are implemented. Execution remains disabled until an independently reviewed runtime adapter proves enforcement.

### Phase C — federated validation

- Capability-aware scheduler with redundant assignment.
- Signed manifests, signed result provenance, replay protection, revocation, quarantine, and human promotion.
- No remote shell and no arbitrary public code.

### Phase D — incentives

- Only after scientific demand, security review, contribution terms, data rights, tax/payment compliance, dispute handling, and anti-Sybil controls exist.
- Funding must never purchase a scientific conclusion.

## Commercialization boundary

A future paid service is compatible with an open evidence project only when participants know, before contributing, what is public, what is private, which license applies, how data may be used, whether compensation exists, and how they can withdraw from future collection. Do not collect production telemetry or invite uncompensated commercial work under ambiguous terms.
