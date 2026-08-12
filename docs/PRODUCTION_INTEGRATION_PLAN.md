# Production integration plan

## Decision

Ship two products with separate trust boundaries:

1. **Public evidence site** — static, globally readable, no credentials, no database, no user uploads, and no executable submissions.
2. **Controlled research service** — authenticated metadata intake, private artifact quarantine, human review, and eventually bounded isolated execution.

Do not turn the static site into the worker coordinator. A compromise of the public presentation layer must not expose contributor records, signing authority, artifact storage, or compute credentials.

## Fastest credible production path

### Release 0 — public site

This release can ship before physical validation because it makes no quieter-system claim.

| Integration | Purpose | Current decision | Production gate |
|---|---|---|---|
| GitHub protected `main` | Reviewed source and release record | Keep | Require the complete release contract, both CodeQL analyses, both supported Python jobs, resolved conversations, and one code-owner approval |
| Vercel Git integration | Preview deployments and production delivery | Repair and confirm ownership | Local repository is linked to the intended project and the project is visible to the active Vercel team |
| Vercel Deployment Checks | Separate a successful build from release | Add | Production alias waits for required GitHub checks and the synthetic monitor |
| Checkly | Public uptime and critical-path checks | Add first from the live `monitoring` Marketplace category | Monitor `/`, `/challenge/`, `/contribute/`, `robots.txt`, and `build-manifest.json` |
| Vercel runtime/access logs | Deployment and request diagnosis | Enable baseline | Post-deploy error scan and incident runbook exist |
| Vercel Web Analytics and Speed Insights | Measure reach and real-user performance | Optional after privacy text is updated | Collect product usage only; never treat engagement as scientific evidence |
| Vercel Firewall | DDoS and staged request controls | Keep platform protection; add API rules only when APIs exist | New rules start in log mode and are reviewed before enforcement |

The August 12, 2026 audit found that GitHub CI, CodeQL, Dependabot, secret scanning, push protection, linear history, review requirements, and force-push protection are active. The only required branch status is currently `Public release contract`; the other science and CodeQL jobs should also become required. Required commit signing is not active, and the existing feature-branch commits are unsigned. Configure signing for future work before enabling that rule; do not rewrite scientific history merely to manufacture verification.

The active Vercel connector can see team `halalmfs-projects` but currently returns no projects, while historical GitHub checks reference `halalmfs-projects/thecubedz`. Treat the project connection as unverified until the local checkout is linked and the project is visible from the account that will own production.

### Release 1 — invited measurement pilot

Provision integrations before installing their SDKs. The required order is `categorize → discover → install → pull environment → build`.

| Integration | Purpose | Data allowed | Data forbidden |
|---|---|---|---|
| Clerk | Operator login and role binding | Account ID, verified email, organization membership | Worker private keys, scientific authority |
| Neon Postgres | Ordered metadata, consent, review state, idempotency, and audit events | Artifact digests, public IDs, workflow state, declared conflicts | Raw sensor files, signing secrets |
| Vercel Blob with private access | Quarantine raw artifacts | Content-addressed approved media types with size and digest metadata | Executables, opaque archives, credentials |
| Resend | Submission receipts and review notices | Minimum delivery metadata | Scientific results not yet authorized for release |

Keep Git as the public release record. PostgreSQL is the operational ledger; it does not silently promote an artifact into canonical science. Private Blob objects remain quarantined until schema, media type, size, digest, consent, license, provenance, and human-review checks pass.

The V0 intake should accept only declared JSON, CSV, and WAV artifacts. Reject executables and opaque archives. Hash locally before upload, use short-lived upload authorization, verify the server-observed digest, and never execute uploaded content.

### Release 2 — controlled compute pilot

This is not required to gather the first baselines.

| Integration | Purpose | Constraint |
|---|---|---|
| Durable workflow provider | Retryable review and validation orchestration | The live Marketplace currently lists Inngest first for `workflow`; re-run discovery immediately before provisioning |
| Vercel Sandbox | Ephemeral execution for frozen jobs | Fixed operations only, immutable snapshot, deny-all network during compute, bounded CPU/memory/disk/time/output, destruction after result capture |
| OIDC-backed key service | Short-lived service identity and result signing | No long-lived signing key in source, a browser, a job manifest, or worker input |
| External application monitoring | Exceptions, traces, and release correlation | Re-run the live `observability` discovery when the API exists; do not add a provider to a static-only site without a measured need |

Queue and workflow delivery is at least once. Every handler must use the signed job digest as an idempotency key, claim it atomically, and produce the same terminal record when retried. A queue acknowledgement is operational state, not scientific approval.

Sandbox isolation does not make arbitrary code acceptable. The existing declarative operation allowlist remains authoritative. Dependencies are installed into a reviewed snapshot before the network policy changes to deny-all; the untrusted phase receives no credentials and no production mounts.

## Product focus

The shortest route to opportunity is not a general scientific marketplace. It is a narrow **Quiet Compute measurement and intervention pilot**:

1. recruit 3–5 server or facility operators;
2. freeze one Round 0 passport with an acoustics/thermal reviewer;
3. publish at least one complete baseline;
4. test one intervention under matched workload;
5. obtain one genuinely independent reproduction;
6. publish the evidence packet, including failures and costs.

The primary operating metric is **reviewable baselines produced per week**. Supporting metrics are time to first valid artifact, complete-provenance rate, rejection reasons, independent-reproduction count, and intervention comparisons satisfying every guardrail. Traffic, followers, funding, compute donated, and reputation scores do not increase scientific authority.

## Explicitly deferred

- payments, bounties, tokens, or percentage-of-prize economics;
- unrestricted public workers or remote shells;
- automatic upload from the bootstrap command;
- AI-generated scientific promotion;
- a graph or vector database as the source of truth;
- a mobile application;
- a microservice split beyond the public site, control plane, and isolated compute boundary;
- public claims about quieter systems, superconductors, or commercial savings before reviewed physical evidence exists.

## Promotion gates

### Gate P0 — public site

- feature branch is pushed and reviewed;
- full release and CodeQL checks pass on the exact remote commit;
- Vercel project ownership and production domain are confirmed;
- preview paths and headers pass synthetic checks;
- rollback is tested;
- production logs are scanned after promotion.

### Gate P1 — invited intake

- contribution terms and privacy notice receive legal review;
- Clerk, Neon, private Blob, and Resend resources are provisioned in the production project;
- roles are deny-by-default;
- artifacts are quarantined and never executed;
- deletion, withdrawal, correction, incident, backup, and restore paths are tested;
- a named reviewer must promote every public artifact.

### Gate P2 — controlled compute

- concrete sandbox adapter passes an independent security assessment;
- network denial, runtime digest, replay, quota, decompression, path escape, output size, and termination tests pass;
- signing-key custody and rotation are documented and exercised;
- a canary worker handles only frozen internal jobs;
- public enrollment remains disabled.

### Gate P3 — public distributed execution

- at least two outside operators reproduce the frozen process;
- incident response and emergency disable controls are exercised;
- abuse, privacy, export-control, and commercial-use review is complete;
- cost caps and per-identity quotas are enforced;
- a named human release decision explicitly enables the feature.

## Operator commands

Run the local production preflight without revealing secret values:

```bash
npm run preflight:production
npm run preflight:production -- --stage intake
npm run preflight:production -- --stage compute --json
```

The preflight is intentionally separate from `npm run check`: scientific reproduction must remain offline and deterministic, while production readiness depends on local links, remote state, and provisioned services.

The ordered implementation prompts are in [`prompts/PRODUCTION_INTEGRATION_PROGRAM.md`](../prompts/PRODUCTION_INTEGRATION_PROGRAM.md).
