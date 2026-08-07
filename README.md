# TheCubedz

> **TheCubedz** is a public, open-source computational experiment for representing spacetime candidates, checking narrowly defined properties, preserving failures, inviting independent challenge, and learning where to investigate next.

[![Status: public pre-alpha](https://img.shields.io/badge/status-public%20pre--alpha-f5a623)](#current-public-status)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-4c8bf5)](LICENSE)
[![Scientific claims: bounded](https://img.shields.io/badge/scientific%20claims-bounded-64e9e4)](docs/SCIENTIFIC_CLAIMS_POLICY.md)
[![Contributions: welcome](https://img.shields.io/badge/contributions-welcome-b8f16d)](CONTRIBUTING.md)

## What this is

Imagine physics as the rulebook for a Rubik's Cube.

A candidate is one arrangement. A validator checks only the rules it explicitly implements. A result records what passed, what failed, what remains unknown, and exactly how the calculation was produced. Failures stay visible so the project gradually builds a map of explored and unexplored regions.

Conventional spaceflight asks:

> How do we move a vehicle across the distance between Earth and Mars?

This project asks a different methodological question:

> Can a reproducible computational system search mathematically defined configurations of geometry, matter, fields, and boundary conditions—and record exactly why candidates fail or survive?

Earth → Mars is a motivating benchmark, **not a transportation claim**.

## What this is not

This repository does **not** demonstrate a wormhole, warp device, faster-than-light travel, a route to Mars, or practical spacetime engineering.

Candidate 000001 is intentionally ordinary: the Minkowski Cartesian flat-spacetime baseline. Its purpose is to test the research instrument before the project attempts anything exotic.

## Current public status

As of **August 7, 2026**, the repository contains:

| Component | Implemented state |
|---|---|
| Candidate registry | Candidate 000001 in a versioned JSON schema |
| Deterministic science core | Exact rational matrix operations and one scoped Minkowski validation profile |
| Baseline result | 12 implemented checks pass; 0 fail |
| Scientific fingerprint | `sha256:91b67470ddfade1770e76793fef54d2f3812ad41f726bda16a3246fb2b428b4b` |
| Reports | Beginner and technical reports derived from the same result object |
| Second brain | Append-only event ledger plus a versioned evidence-graph projection |
| Agent contracts | 9 bounded research roles with explicit permissions and prohibitions |
| Controlled autonomy | Machine-validated task, capability, run, evidence-bundle, and human-promotion contracts |
| Synthetic benchmark | 100 frozen workflow cases: 23 accepted, 57 rejected, 5 mismatches preserved, and 15 unresolved |
| Cross-check | 1 separate standard-library implementation path matches all 12 baseline checks; not an outside reproduction |
| Public website | 8 responsive routes, six-face evidence cube, interactive lab, evidence graph, learning layer, roadmap, and contribution paths |
| Automated validation | Scientific, control-contract, benchmark, cross-check, artifact, static-site, link, base-path, and build-fingerprint checks |
| Independent reproductions | 0 recorded |
| Novel physics claims | 0 |

The baseline statement is deliberately narrow:

> The exact submitted Minkowski Cartesian benchmark passed every implemented V0 check. This verifies the baseline pipeline—not a general relativity solver or transportation capability.

## See the public laboratory locally

### Requirements

- Python 3.12 or newer
- Node.js 20.9 or newer; Node 22 is used by the launch workflow
- Git

### Clean setup

```bash
git clone <repository-url>
cd <repository-directory>

python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --no-build-isolation -e '.[dev]'

npm ci
npm run check
```

### Run the website

```bash
npm run dev
```

Open `http://127.0.0.1:4173`.

### Reproduce Candidate 000001

```bash
python scripts/research.py verify candidates/CANDIDATE-000001.json --reproducible
```

A matching repository run should emit the published scientific payload digest. Re-running the same implementation is useful software verification; it is **not yet independent scientific reproduction**.

### Run the frozen workflow benchmark and separate implementation path

```bash
python scripts/research.py benchmark
python scripts/independent_crosscheck.py
```

The 100-case suite validates the research workflow, security boundaries, and explicit unresolved states. The separate implementation uses a different exact matrix algorithm, but it shares this repository, environment, and project authorship, so it does not count as an outside reproduction.

## One command before every push

```bash
npm run check
```

That command performs the canonical baseline verification, Python tests, static website build, artifact reconciliation, internal-link validation, responsive/base-path checks, and build-manifest verification.

## Deploy today

### Vercel

1. Create a new **empty public GitHub repository**. Do not initialize it with another README, license, or `.gitignore`.
2. Configure your GitHub-verified author name/email and create one empty ownership commit, as shown in [the launch runbook](docs/LAUNCH.md).
3. Push the supplied history and its existing release tag to the new repository. Do not recreate or move `v0.1.0-alpha.1`.
4. In Vercel, create a project and import the GitHub repository.
5. Vercel reads `vercel.json`, runs `npm run build`, and publishes `dist/`.
6. Set these optional public build variables:

```text
PUBLIC_REPOSITORY_URL=https://github.com/chefmrfrizzle/TheCubedz
PUBLIC_SITE_URL=https://<deployment-domain>
PUBLIC_CONTACT_URL=https://github.com/chefmrfrizzle/TheCubedz/discussions
```

7. Redeploy after adding `PUBLIC_SITE_URL` so canonical URLs and the sitemap use the production domain.

### GitHub Pages

The included Pages workflow builds the correct repository base path automatically. After pushing:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, select **GitHub Actions**.
3. Run or re-run the `Deploy public laboratory` workflow.

See [docs/LAUNCH.md](docs/LAUNCH.md) for the exact push, Vercel, GitHub Pages, rollback, and post-launch commands.

## Scientific architecture

```text
question / source / candidate / challenge / reproduction / telemetry
                              │
                              ▼
                 schema + provenance validation
                              │
                              ▼
                   append-only event ledger
                              │
              ┌───────────────┴────────────────┐
              ▼                                ▼
       evidence graph                  frozen dataset snapshot
              │                                │
              ▼                                ▼
    public exploration                offline model training
              │                                │
              └───────────────┬────────────────┘
                              ▼
                     frozen benchmark suite
                              │
                              ▼
                       human promotion
                              │
                              ▼
                  next-experiment proposal
                              │
                              └── returns to working memory
```

The **ledger is the source of truth**. The graph is a rebuildable projection. Models are replaceable consumers of frozen snapshots.

Read:

- [Architecture](docs/ARCHITECTURE.md)
- [Second brain](docs/SECOND_BRAIN.md)
- [Knowledge graph](docs/KNOWLEDGE_GRAPH.md)
- [Data governance](docs/DATA_GOVERNANCE.md)
- [Scientific claims policy](docs/SCIENTIFIC_CLAIMS_POLICY.md)
- [Threat model](docs/THREAT_MODEL.md)

## Three memory tiers

### A. Canonical science

Versioned candidates, deterministic results, reviewed evidence, reproductions, corrections, and retractions. Only explicit evidence gates may change scientific status.

### B. Working research

Hypotheses, unresolved paper extractions, agent proposals, candidate drafts, anomaly queues, and challenge records. These objects may guide work; they are not established facts.

### C. Product telemetry

Explanation-level choices, failed searches, voluntary clarity ratings, accessibility friction, and performance data. These signals may improve the interface. They may never determine whether physics is correct.

## Controlled learning—not magical self-training

The “second brain” does not continuously believe and retrain on public activity.

A model or search policy may be promoted only after:

1. a named, immutable dataset snapshot;
2. license and provenance checks;
3. leakage-resistant train/evaluation splits;
4. comparison against a naive baseline and current champion;
5. calibration, regression, reproducibility, cost, and safety tests;
6. a model card;
7. human approval; and
8. a tested rollback target.

The first learned component should not be a grand “physics AI.” It should be a bounded search-policy experiment answering a measurable question:

> Given a frozen benchmark space, can the policy choose more informative next evaluations than random or hand-written baselines at the same compute budget?

## Agent operating system

Agents are specialized workers, not scientific authorities.

| Role | Primary output | Can change canonical scientific status? |
|---|---|---:|
| Orchestrator | Typed task and handoff records | No |
| Literature agent | Cited evidence proposals | No |
| Candidate agent | Schema-conforming candidate draft | No |
| Math/GR agent | Deterministic solver job and result proposal | No |
| Skeptic agent | Challenges and failure tests | No |
| Reproduction agent | Clean-run comparison record | No |
| Explainer agent | Multi-level explanation from one verified artifact | No |
| Search-policy agent | Ranked next-experiment proposals | No |
| Graph curator | Merge/supersession proposals | No |

Every handoff must contain explicit inputs, output schema, authority level, prohibited actions, validation commands, and a definition of done.

Read [docs/AGENT_OPERATING_SYSTEM.md](docs/AGENT_OPERATING_SYSTEM.md) and use the copy-pasteable prompts in [`prompts/`](prompts/).

## Scientific status is multidimensional

Never collapse all evaluation into one “works” score.

A candidate may have separate states for:

- definition and schema validity;
- mathematical consistency;
- numerical convergence;
- stress-energy requirements;
- energy-condition behavior;
- stability;
- causality;
- compatibility with known physical models;
- engineering realizability;
- independent reproduction; and
- experimental support.

A mathematically interesting configuration is not automatically physically admissible, stable, buildable, or useful for transportation.

## Success ladder

| Level | Evidence earned |
|---:|---|
| 0 | Reproduce a simple baseline correctly. |
| 1 | Recover known properties and known failure modes. |
| 2 | Cross-check established metrics with independent validator or solver adapters. |
| 3 | Search a bounded benchmark more efficiently than a declared naive baseline. |
| 4 | Identify mathematically interesting regions worth expert review. |
| 5 | Produce a novel result that survives independent reproduction. |
| 6 | Connect a theoretical requirement to a plausible physical model. |
| 7 | Make a measurable experimental prediction. |
| 8 | Obtain independent experimental confirmation. |

A rigorous negative result is a success when it maps a region that need not be searched again under the same assumptions.

## Repository layout

```text
.
├── candidates/                  # Versioned candidate definitions
├── artifacts/                   # Canonical result and human-readable reports
├── data/
│   ├── knowledge-graph.json     # Rebuildable graph snapshot
│   ├── agents.json              # Public agent contracts
│   ├── roadmap.json             # Machine-readable roadmap
│   └── ledger/events.jsonl      # Append-only research events
├── docs/                        # Science, architecture, governance, launch, and ADRs
├── prompts/                     # Bounded copy-pasteable agent prompts
├── scripts/
│   ├── research.py              # Scientific CLI entry point
│   ├── build_site.mjs           # Deterministic static-site builder
│   ├── test_site.mjs            # Website release validator
│   └── serve_site.mjs           # Local static preview server
├── src/
│   ├── core/                    # Versioned JSON schemas
│   └── research_core/           # Deterministic baseline implementation
├── tests/                       # Scientific and data-contract tests
├── web/                         # Dependency-free public interface source
├── package.json                 # Website build, test, and release commands
├── pyproject.toml               # Python package and test configuration
└── vercel.json                  # Static deployment and security headers
```

## Why a dependency-free public site?

The public alpha is intentionally static:

- no account system;
- no database;
- no untrusted code execution;
- no live model calls;
- no secret keys;
- no hidden backend state.

This makes the launch cheap, auditable, forkable, and deployable on Vercel, GitHub Pages, or any static host. Heavy compute, authentication, queues, and sandboxes arrive only when measured demand and security requirements justify them.

## High-value future features

The roadmap preserves ambitious ideas without presenting them as implemented:

- a searchable failure atlas;
- uncertainty and contradiction maps;
- cross-solver reproduction passports;
- adversarial challenge and falsification records;
- signed federated compute bundles;
- transparent search-policy tournaments;
- a multi-level explanation compiler;
- benchmark-gated model promotion;
- provenance-preserving literature ingestion;
- portable forks of the candidate → validator → artifact → graph → search loop for other scientific domains.

See [docs/INNOVATION_BLUEPRINT.md](docs/INNOVATION_BLUEPRINT.md).

The next controlled-autonomy milestone is specified in:

- [Thesis and research program](docs/THESIS_AND_RESEARCH_PROGRAM.md)
- [Controlled autonomy blueprint](docs/CONTROLLED_AUTONOMY_BLUEPRINT.md)
- [Synthetic benchmark v1: 100 workflow cases](docs/SYNTHETIC_BENCHMARK_100.md)
- [Security standards baseline](docs/SECURITY_STANDARDS_BASELINE.md)
- [GitHub security settings record](docs/GITHUB_SECURITY_SETTINGS.md)
- [Step-by-step controlled autonomy build prompts](prompts/CONTROLLED_AUTONOMY_BUILD_PROGRAM.md)

## Contribution paths

You do not need to solve an exotic physics problem to help.

Useful first contributions include:

- reproduce Candidate 000001 from a clean environment;
- identify a hidden assumption or convention mismatch;
- improve accessibility or plain-language explanation;
- add schema failure tests;
- review claims and provenance;
- propose the next established benchmark;
- implement a second independent baseline validator;
- improve threat modeling or sandbox design;
- validate the website on another browser or device.

Read [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Project principles

1. **AI explores. Physics referees. Reproduction decides what survives.**
2. **No result without provenance.**
3. **A validator may claim only the checks it implements.**
4. **Failure is permanent, searchable data.**
5. **Unknown stays unknown.**
6. **Mathematics, physical admissibility, stability, causality, and engineering are separate.**
7. **Popularity never changes scientific status.**
8. **Benchmarks before novelty.**
9. **Version the candidate, validator, result, dataset, model, prompt, and explanation.**
10. **Make extraordinary claims harder to publish than ordinary corrections.**

## License and citation

Source code and project documentation are available under the [Apache License 2.0](LICENSE). See [CITATION.cff](CITATION.cff) for citation metadata and [NOTICE](NOTICE) for attribution guidance.
