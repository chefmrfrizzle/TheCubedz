# Controlled autonomy blueprint

## Meaning of "self-building"

TheCubedz may automate proposal, implementation on an isolated branch, testing, criticism, comparison, and preparation of a review packet. It may not autonomously change canonical science, merge to the protected branch, publish a scientific status, expand its own permissions, or train on unreviewed public activity.

The safe loop is:

```text
bounded question
  -> typed task manifest
  -> least-privilege policy decision
  -> proposal agents in working memory
  -> deterministic tools in an isolated runner
  -> skeptic and security review
  -> independent reproduction when required
  -> evidence bundle and human decision
  -> attested release or permanent rejection record
```

## Current implementation status

Implemented in `0.2.0-alpha.1`:

- machine-validated research-task, capability-envelope, agent-run, evidence-bundle, and promotion-decision contracts;
- policy checks for expiry, denied-network consistency, traversal, canonical write paths, agent release claims, and self-approval;
- a frozen 100-case workflow benchmark with explicit accept, reject, mismatch, and unresolved outcomes;
- a separate standard-library baseline implementation and comparison passport;
- an artifact-driven six-face evidence cube with keyboard controls and a semantic summary;
- pinned GitHub Actions, Pages build provenance attestation, protected `main`, secret scanning, push protection, vulnerability alerts, and automated security updates.

Not implemented or not claimable yet:

- an outside clean-environment reproduction;
- a general tensor or numerical-relativity solver;
- a hosted agent control plane, authentication service, queue, or public sandbox;
- live model calls, autonomous pull requests, or autonomous releases;
- a validated search policy or novel spacetime candidate.

The static public site remains read-only. This is intentional: public agent execution is gated until the contracts and threat controls have independent review.

## System planes

| Plane | Responsibility | Initial implementation |
|---|---|---|
| Public | Read-only site, cube, raw artifacts, methods, limitations | Static files only; no credentials or model calls |
| Contribution | Structured questions, challenges, and reproduction manifests | GitHub issue forms and pull requests with schema validation |
| Control | Task compiler, policy checks, queue, approval state | Repository contracts and CI before any hosted service |
| Execution | Deterministic jobs and bounded agent work | Ephemeral CI job; future hardened sandbox for untrusted jobs |
| Evidence | Content-addressed outputs, logs, comparisons, ledger events | Versioned files and append-only event records |
| Release | Human approval, protected branch, build provenance, rollback | GitHub branch rules, pinned workflows, artifact attestations |
| Monitoring | Audit log, abuse detection, incident response, kill switch | Workflow logs, security reporting, manual disable path |

Keep this a modular monolith until real load, isolation, or ownership data justifies a service boundary.

## Authority model

Every operation receives a capability envelope containing:

- task and run identifiers;
- actor and agent role;
- immutable input hashes;
- allowed tools and commands;
- allowed read and write paths;
- network policy;
- CPU, memory, duration, and output limits;
- required validators;
- approval requirements;
- expiry time;
- parent run and prompt versions.

Anything not explicitly granted is denied. An agent cannot edit its envelope, approve its own output, or write directly to canonical directories.

## State machine

```text
DRAFT
  -> PREFLIGHT_REJECTED
  -> APPROVED_FOR_WORK
      -> RUNNING
          -> FAILED
          -> REVIEW_REQUIRED
              -> CHANGES_REQUESTED
              -> REJECTED
              -> APPROVED_FOR_REPRODUCTION
                  -> REPRODUCTION_MISMATCH
                  -> APPROVED_FOR_PROMOTION
                      -> RELEASED
                      -> ROLLED_BACK
```

There is no model-controlled transition to `APPROVED_FOR_PROMOTION`, `RELEASED`, or a canonical scientific claim status.

## Minimum agent set

Use the current roles. Do not add an agent when a deterministic function or review checklist is enough.

| Role | Produces | Cannot do |
|---|---|---|
| Orchestrator | Task plan and handoff envelopes | Invent conclusions or approve promotion |
| Science/candidate | Definitions, assumptions, candidate drafts | Declare physical possibility |
| Build | Code and tests on an isolated branch | Change claims without evidence |
| Skeptic | Counterexamples and falsification tests | Suppress inconvenient failures |
| Security review | Threat findings and a release recommendation | Waive scientific or reproduction gates |
| Reproduction | Independence declaration and comparison | Call the same code an independent implementation |
| Explainer | Audience-specific views of one artifact | Change the source result |
| Search policy | Ranked experiment proposals | Mark its own choices successful |
| Release | Attested review packet and release instructions | Merge or release after any required gate fails |

Separate prompts and model contexts reduce correlated mistakes, but they do not create independent scientific evidence.

## Public user modes

### Safe for the first interactive release

- Explain a committed artifact at a selected technical level.
- Trace a public claim to its inputs, validator, tests, and limitations.
- Compare two committed results field by field.
- Draft a falsification question through a bounded form.
- Prepare a schema-valid candidate or reproduction manifest without executable code.
- Download a reproducible evidence bundle.

Every generated response is labeled `WORKING MEMORY` and carries prompt, model, source-artifact, and timestamp metadata. It cannot write to the ledger.

### Not safe for the first interactive release

- Arbitrary shell, Python, notebook, package installation, or uploaded executables.
- Browser-held API keys or server credentials exposed through `PUBLIC_*` values.
- An unrestricted general-purpose chat agent with repository write access.
- Automatic merge, release, claim promotion, or continuous self-training.
- Network-enabled execution of contributor code.

## Execution isolation requirements

Before any public job runner exists, it must provide:

1. ephemeral non-root workers;
2. no network by default and an explicit destination allowlist when needed;
3. read-only mounted inputs identified by digest;
4. a disposable writable workspace outside canonical storage;
5. pinned runtime images and dependencies;
6. CPU, memory, process, time, disk, and output quotas;
7. syscall and filesystem restrictions appropriate to the runtime;
8. no deployment, repository-write, or secret-bearing token;
9. output type, size, path, and malware validation;
10. signed job manifest, complete logs, and provenance attestation;
11. immediate revocation and queue-wide kill switch;
12. manual promotion of reviewed outputs only.

## Evidence bundle

Every completed run should emit one content-addressed bundle containing:

- task manifest and policy decision;
- exact source commit and dirty-tree state;
- prompt and model identifiers for agent-generated material;
- environment and dependency lock digests;
- stdout, stderr, exit codes, and timings;
- input and output hashes;
- deterministic test results;
- skeptic and security findings;
- reproduction comparison when required;
- limitations, unresolved contradictions, and downgrade conditions;
- human decision and reviewer identity;
- build provenance and release target when promoted.

## Promotion gates

| Change type | Required gates |
|---|---|
| Documentation or explanation | Source reconciliation, claims check, accessibility, human review |
| Software without scientific-output change | Tests, security review, artifact-drift check, human review |
| Validator or schema change | Positive/negative/boundary tests, benchmark replay, scientific review, security review |
| Scientific result change | All prior gates plus skeptic review and reproduction policy |
| Agent/tool permission change | Threat-model update, abuse tests, dual human approval, rollback drill |
| Search-policy promotion | Frozen holdout, baseline comparison, calibration, model card, human approval |

## Security priorities

1. Protect credentials and release authority.
2. Protect canonical scientific history and provenance.
3. Prevent untrusted execution and resource abuse.
4. Prevent claim injection through presentation or generated text.
5. Preserve privacy and minimize telemetry.
6. Make shutdown, rollback, correction, and retraction routine operations.

## Success metrics

- zero unauthorized canonical transitions;
- 100% of runs have complete input/output provenance;
- 100% of promoted scientific changes have the required review records;
- benchmark expected-versus-observed accuracy by class;
- mismatch discovery rate and time to resolution;
- reproduction coverage by independence level;
- explanation claim-fidelity rate;
- search-policy information gain per unit of compute against frozen baselines;
- sandbox escapes, secret exposures, and uncontrolled network calls: zero.
