# Production integration build program

Use one prompt at a time. Do not start a later prompt by weakening an earlier gate. Every implementation must preserve the Quiet Compute rules: no automatic upload, no arbitrary public code, no scientific majority vote, no purchased scientific authority, and named human promotion.

## Prompt 1 — repair and gate the public release

```text
Act as the production release engineer for TheCubedz. Audit the current feature branch, PR, protected main branch, GitHub Actions, Vercel Git connection, deployment project ownership, domain, environment settings, headers, and rollback path. Push only the intentional commits after showing the staged scope. Make the complete release contract, supported Python jobs, both CodeQL analyses, and a synthetic production monitor required before release. Configure Vercel so a successful build is staged until deployment checks pass. Do not create or expose long-lived tokens, do not bypass branch protection, and do not publish a firewall draft. Return the exact remote commit, PR checks, preview URL, production target, rollback command, and remaining blockers.
```

## Prompt 2 — provision the minimum external services

```text
Act as the integration provisioner for the invited Quiet Compute measurement pilot. Start by linking the intended Vercel project, then use the live Vercel Marketplace sequence categorize → discover → install. Provision Clerk for operator identity, Neon for operational metadata, private Vercel Blob for quarantined artifacts, Resend for transactional receipts, and Checkly for synthetic monitoring. Stop for any account-claim or billing confirmation that requires the owner. Pull environment variables only after each resource is installed. Show environment-variable names but never values. Do not install an SDK or scaffold provider code before the corresponding real resource exists. Do not provision payments, AI, a vector database, or public compute.
```

## Prompt 3 — build the authenticated intake control plane

```text
Act as the security-focused control-plane engineer. Keep the existing static public site intact and build a separate authenticated intake service. Implement Clerk roles for operator, reviewer, security responder, and release manager with deny-by-default authorization. Use Neon for append-only intake events, consent versions, conflict disclosures, review state, idempotency claims, and artifact metadata. Use private Blob for content-addressed JSON, CSV, and WAV only. Require short-lived upload authorization, strict MIME and extension agreement, byte limits, digest verification, duplicate detection, raw filename neutralization, no executables, no opaque archives, no automatic publication, and no execution. Create migration, rollback, backup, restore, deletion, withdrawal, and correction tests. A database status must never bypass signed artifact validation or named human promotion.
```

## Prompt 4 — add production observability without contaminating science

```text
Act as the reliability engineer. Add structured logs with request IDs, route, duration, status, actor ID hash, artifact digest, and failure code; never log raw artifacts, emails, credentials, tokens, cookies, or scientific payload bodies. Configure Checkly checks for the homepage, challenge, contribute page, robots.txt, build manifest, authentication health, and a non-mutating intake preflight. Add deployment-time preview checks, post-deploy error scanning, uptime alert routing, and an incident runbook. If product analytics is enabled, update the privacy notice and keep product telemetry in a separate tier that cannot alter scientific status. Stage firewall and rate-limit rules in log mode first and require the owner to publish them after traffic review.
```

## Prompt 5 — implement durable, idempotent review workflows

```text
Act as the workflow engineer. Re-run live Marketplace discovery for the workflow category and provision the selected provider before adding its SDK. Implement an outbox-backed, at-least-once pipeline for SUBMISSION_RECEIVED → PREFLIGHT_PASSED/FAILED → REVIEW_REQUESTED → REVIEW_DECIDED → PUBLICATION_REQUESTED. Messages carry IDs and digests, not raw artifacts or secrets. Atomically claim every signed job digest, make handlers idempotent, bound retries, quarantine poison messages, preserve every failure, and expose backlog age and terminal-state metrics. Queue acknowledgement is not scientific approval. Add crash, duplicate delivery, reordering, timeout, partial write, and provider outage tests.
```

## Prompt 6 — connect the existing job planner to an isolated pilot

```text
Act as the untrusted-compute security engineer. Integrate the existing signed declarative Quiet Compute job admission and plan-only isolation output with Vercel Sandbox for internal frozen jobs only. Use a reviewed immutable snapshot, install dependencies before lockdown, switch to deny-all network for the compute phase, expose no credentials, mount inputs read-only, use ephemeral scratch storage, enforce CPU/memory/disk/time/output quotas, and destroy the sandbox after capture. Permit only VALIDATE_MEASUREMENT, COMPARE_MEASUREMENTS, and REPRODUCE_FROZEN_BENCHMARK. Preserve Ed25519 envelope verification, external trust-store revocation, atomic replay claims, result signatures, and declared conflict of interest. Test path escape, runtime substitution, decompression bombs, fork bombs, output floods, network attempts, metadata service access, replay, cancellation, and cleanup. Do not enable public enrollment.
```

## Prompt 7 — conduct the production security review

```text
Act as an independent application-security reviewer. Review authentication, authorization, tenancy, artifact upload, Blob access, database row isolation, webhook and drain signatures, queue idempotency, sandbox network policy, secret handling, key rotation, logs, backups, deletion, dependency supply chain, GitHub protections, Vercel deployment checks, firewall rules, rate limits, rollback, and emergency shutdown. Construct adversarial tests and record evidence for every control. Report APPROVED, CHANGES_REQUIRED, or REJECTED with exact file, configuration, command, and observed output references. Do not treat vendor marketing, passing unit tests, or same-owner agreement as an independent security assessment.
```

## Prompt 8 — run the first invited evidence pilot

```text
Act as the Quiet Compute pilot operator. Recruit 3–5 invited server or facility operators. Freeze the reviewed Round 0 passport before accepting measurements. Walk each operator through local collection, deliberate artifact selection, consent, conflict disclosure, and signed submission. Track time to first valid artifact, provenance completeness, rejection reason, measurement uncertainty, and reviewer workload. Publish no raw artifact outside its declared scope. Produce one reviewed baseline, one matched intervention comparison, and one genuinely independent reproduction before expanding recruitment or discussing bounties.
```

## Prompt 9 — make the release decision

```text
Act as the named release manager. Run npm run check and npm run preflight:production on a clean clone of the exact remote commit. Confirm all required GitHub checks, Vercel deployment checks, synthetic monitors, production environment protections, privacy and contribution terms, incident contacts, rollback, backup restore, and current scientific-status language. Promote the staged production deployment only if every P0/P1 gate in docs/PRODUCTION_INTEGRATION_PLAN.md is satisfied. After promotion, verify the domain and critical paths, scan production errors, record the deployment ID and commit, and keep a tested rollback target. Never enable public execution as part of this release.
```

## Stop conditions

- Stop deployment if the active Vercel account cannot see and own the target project.
- Stop provider code if the corresponding Marketplace resource is not installed.
- Stop intake if privacy, consent, withdrawal, deletion, license, or commercial-use rules are unresolved.
- Stop execution if deny-all network, quotas, replay storage, runtime pinning, result signing, or emergency termination is unverified.
- Stop a scientific claim if the workload differs, required measurements are missing, or outside reproduction has not occurred.
- Stop monetization if payment incentives can be confused with evidence reputation or scientific authority.
