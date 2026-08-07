# Threat model

## Scope

This document covers the public static site, repository workflows, scientific artifacts, agent-assisted contributions, and future community compute.

## Protected assets

1. Integrity of canonical candidates and result artifacts.
2. Provenance and status history in the append-only event ledger.
3. Contributor identity and review records.
4. CI and deployment credentials.
5. Dataset licenses and source attributions.
6. Public trust in the distinction between hypothesis, computation, reproduction, and experiment.

## Current V0 trust boundary

V0 has no authentication, database, secret-bearing browser code, remote model call, or public job runner.

```text
untrusted visitor
      │
      ▼
static HTML/CSS/JS ──read only──▶ committed JSON/Markdown artifacts
```

The browser-side matrix cross-check is convenience output. It cannot change canonical state.

## Principal threats

### Scientific status injection

**Threat:** A contributor edits presentation text to upgrade a hypothesis or generated output into an established result.

**Controls:** Claims policy, artifact reconciliation tests, protected branch, code review, visible limitations, and separate candidate/result statuses.

### Evidence poisoning

**Threat:** Fabricated citations, licensed material used improperly, or repeated agent output enters the canonical graph.

**Controls:** Source-location fields, extraction status, license fields, human curation, frozen snapshots, and an anti-loop rule preventing generated repetition from becoming truth.

### Generated-artifact drift

**Threat:** The website, report, graph, and result disagree.

**Controls:** One result object, generated reports, project-status reconciliation, full scientific digest display, and build-manifest hashes.

### Supply-chain compromise

**Threat:** A dependency or GitHub Action is compromised.

**Controls:** Minimal runtime dependencies, committed lockfile, Dependabot, CodeQL, least-privilege workflow permissions, and future pinning of high-impact actions to reviewed commit SHAs.

### Workflow-secret exposure

**Threat:** Deployment or API credentials are committed or printed.

**Controls:** No V0 secrets, `.env` ignored, public variables clearly marked, GitHub secret scanning, no pull-request workflow with write credentials.

### Untrusted code execution

**Threat:** A community candidate includes executable code that runs on shared infrastructure.

**V0 control:** Community code is not executed by the website.

**Future controls:** isolated microVM/container runner, no network by default, read-only inputs, CPU/memory/time quotas, ephemeral filesystem, syscall filtering, signed job manifest, output-size limits, malware scanning, provenance attestation, and manual promotion.

### Resource abuse

**Threat:** Public compute is used for unrelated workloads or denial of service.

**Future controls:** authenticated contributors, quotas, bounded schemas, preflight static analysis, queue isolation, rate limits, sponsorship budgets, and kill switches.

### Model/data leakage

**Threat:** A search model sees evaluation answers or private review material.

**Controls:** frozen splits, dataset manifests, role-based snapshot access, no live training, evaluation holdout isolation, and model cards.

### Harassment or pseudo-scientific community capture

**Threat:** Contributors are attacked, extraordinary claims overwhelm careful work, or status becomes a popularity contest.

**Controls:** Code of Conduct, moderated issues/discussions, quality-based contribution records, no financial prediction mechanism, and no engagement-driven scientific ranking.

## Security invariants

- Canonical history is append-only or superseded; never silently overwritten.
- A model cannot approve its own output.
- A browser calculation cannot alter scientific status.
- A public pull request receives read-only default permissions.
- Untrusted executables never run in the deployment environment.
- Telemetry is not a physics label.
- A release can be rebuilt from a clean clone.

## Reporting

Follow [SECURITY.md](../SECURITY.md). Do not open a public issue for a vulnerability that could compromise contributor accounts, CI credentials, deployment control, or future compute isolation.
