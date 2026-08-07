# Open Computational Spacetime Research Project

> **Working title intentionally omitted.** This repository is a blank-brand, open-source foundation for a computational experiment: can systematic search over mathematically defined spacetime configurations help us map which ideas are valid, invalid, unresolved, or worth deeper scientific study?

[![Status: Experimental](https://img.shields.io/badge/status-experimental-orange)](#project-status)
[![License: Apache--2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)](CONTRIBUTING.md)

## The idea in plain English

Imagine that physics is a Rubik's Cube.

You are not allowed to break the cube, remove stickers, or invent new rules. You can only make moves that the laws of physics permit.

Conventional space travel asks: **How do we move a vehicle across the distance between Earth and Mars?**

This project asks a different research question:

> **Can a computer systematically explore allowed mathematical configurations of spacetime, matter, and fields to find configurations with interesting transportation properties — while rigorously recording why most candidates fail?**

This repository does **not** claim that wormholes, warp drives, faster-than-light travel, or practical spacetime engineering are possible. The goal is to build a reproducible search-and-evaluation system that can test ideas rather than merely speculate about them.

## The scientific version

A spacetime can be described by a metric tensor \(g_{\mu\nu}\). General relativity relates spacetime curvature to stress-energy through Einstein's field equations:

\[
G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}.
\]

At a high level, the project treats a candidate spacetime as a parameterized object:

\[
X = \{g_{\mu\nu}, T_{\mu\nu}, \text{matter model}, \text{fields}, \text{boundary conditions}, \theta\}.
\]

The engine then asks:

1. Is the candidate mathematically well-defined?
2. Does it satisfy the required equations to the chosen numerical tolerance?
3. What stress-energy distribution does it imply?
4. What energy conditions are satisfied or violated?
5. Is the candidate numerically stable under perturbation?
6. Does it create causal or other known theoretical problems?
7. Is there any plausible known matter/field model that resembles what it requires?
8. Can another researcher reproduce the result?

The early objective is **not** "find a wormhole." The objective is:

> **Generate → Evaluate → Reject or Retain → Explain → Reproduce → Learn where to search next.**

## What would count as success?

Success comes in levels. The project is useful long before any exotic transportation result exists.

| Level | Success criterion |
|---|---|
| 0 | Reproduce simple benchmark spacetimes correctly. |
| 1 | Reproduce known analyses and known failure modes. |
| 2 | Perturb known families and recover expected nearby behavior. |
| 3 | Search a parameter space more efficiently than naive brute force. |
| 4 | Identify mathematically interesting candidate regions worth expert review. |
| 5 | Produce a novel result that survives independent reproduction. |
| 6 | Connect a theoretical candidate to a plausible physical model. |
| 7 | Make a testable experimental prediction. |
| 8 | Obtain independent experimental confirmation. |

A negative result can still be a successful result if it is reproducible and teaches us something about the search space.

## The first public challenge: Earth → Mars

Mars is a benchmark, not a promise.

The initial challenge is to build an evaluation framework that can compare candidate configurations against conventional baselines and known spacetime families. The project should never label a candidate "Mars-capable" unless the evidence actually warrants that statement.

The first milestone is much smaller:

> **Candidate 000001: Minkowski spacetime. Define it, validate it, visualize it, explain it at multiple levels, and make the result exactly reproducible.**

Then add additional established benchmark metrics one by one.

## Architecture

```text
                     ┌──────────────────────────┐
                     │    Human contributors    │
                     └────────────┬─────────────┘
                                  │
                                  ▼
┌──────────────┐      ┌──────────────────────────┐
│ Literature & │─────▶│  Evidence / knowledge    │
│ datasets     │      │  graph                   │
└──────────────┘      └────────────┬─────────────┘
                                  │
                                  ▼
                       ┌─────────────────────────┐
                       │ Candidate generator      │
                       │ (human + algorithmic)    │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │ Deterministic validators │
                       └────────────┬────────────┘
                                    │
                 ┌──────────────────┼───────────────────┐
                 ▼                  ▼                   ▼
            Math checks       Physics checks      Numerical checks
                 └──────────────────┼───────────────────┘
                                    ▼
                       ┌─────────────────────────┐
                       │ Candidate registry       │
                       │ + provenance + failures  │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │ Search policy / learner  │
                       │ proposes where to look   │
                       │ next                     │
                       └─────────────────────────┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the detailed design.

## The "second brain" — without fake self-learning

The system should **not** silently retrain itself on every click or accept popularity as scientific truth.

Instead, it learns in a controlled loop:

```text
Observation
  ↓
Structured event
  ↓
Evidence/provenance validation
  ↓
Candidate evaluation
  ↓
Human/reproducibility review
  ↓
Versioned dataset snapshot
  ↓
Offline model/search-policy training
  ↓
Benchmark evaluation
  ↓
Promotion only if measurably better
  ↓
New search proposals
```

User activity can help answer questions such as "what explanations are confusing?" or "which candidates deserve independent reproduction?" It must **not** turn votes or engagement into physical truth.

The durable memory should be a versioned knowledge graph and experiment ledger. Machine-learning models are disposable consumers of that evidence, not the source of truth.

Read [docs/LEARNING_LOOP.md](docs/LEARNING_LOOP.md).

## Proposed agent system

Agents are assistants, not scientific authorities.

| Agent | Job | May decide truth? |
|---|---|---|
| Literature Agent | Finds and structures relevant papers/results. | No |
| Candidate Agent | Proposes parameterized candidates. | No |
| GR/Math Agent | Prepares symbolic/numerical tasks and checks. | No; solver output is authoritative for the computation |
| Energy-Conditions Agent | Runs/organizes condition analyses. | No |
| Stability Agent | Designs perturbation and convergence tests. | No |
| Causality Agent | Flags causal structures needing analysis. | No |
| Materials Agent | Maps theoretical requirements to known material/field properties. | No |
| Reproduction Agent | Re-runs exact candidates in clean environments. | No |
| Skeptic Agent | Tries to falsify claims and locate hidden assumptions. | No |
| Explainer Agent | Converts one result into beginner/intermediate/expert explanations. | No |
| Search Agent | Chooses promising next regions under a transparent objective. | No |
| Curator Agent | Proposes dataset additions; humans approve canonical data. | No |

Detailed responsibilities and boundaries are in [docs/AGENTS.md](docs/AGENTS.md).

## Scientific rules

1. **No result without provenance.** Every candidate records equations, parameters, solver version, code commit, environment, tolerances, and references.
2. **No AI-generated claim is automatically evidence.** AI can propose; deterministic computation and reproducible sources must verify.
3. **Failure is permanent data.** Rejected candidates remain searchable.
4. **Unknown means unknown.** Do not translate uncertainty into possibility or impossibility.
5. **Separate mathematics from physical realizability.** A valid solution to equations is not automatically buildable.
6. **Independent reproduction outranks popularity.** Stars, votes, and social engagement never change scientific status.
7. **Benchmarks before novelty.** The system must demonstrate that it can reproduce known results before novel candidate generation matters.
8. **Version everything.** Datasets, code, schemas, models, prompts, and candidate definitions all receive versions/hashes.

## Candidate status model

Suggested initial statuses:

```text
DRAFT
VALIDATING
MATHEMATICALLY_VALID
MATHEMATICALLY_INVALID
PHYSICALLY_PROBLEMATIC
UNRESOLVED
REPRODUCTION_PENDING
REPRODUCED
FALSIFIED
EXPERT_REVIEW
ARCHIVED
```

Never collapse these into a single "works / doesn't work" score.

## Repository layout

```text
.
├── README.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SCIENCE.md
│   ├── AGENTS.md
│   ├── LEARNING_LOOP.md
│   └── ROADMAP.md
├── prompts/
│   ├── BUILD_AGENT.md
│   ├── SCIENCE_AGENT.md
│   ├── SKEPTIC_AGENT.md
│   └── RESEARCH_AGENT.md
├── src/
│   └── core/
│       └── candidate.schema.json
└── tests/
    └── README.md
```

## Recommended technology path

Do **not** start by building a giant AI system.

Start with a deterministic core:

- Python for scientific orchestration and numerical work.
- JSON Schema / Pydantic-style typed candidate records.
- PostgreSQL later for experiment metadata.
- Object storage later for simulation artifacts.
- A web frontend only after the candidate format and validator are stable.
- Containers for reproducible runs.
- CI for schema validation, unit tests, deterministic benchmarks, and reproducibility checks.
- External numerical-relativity tools should be integrated as adapters rather than rewritten from scratch.

Relevant existing scientific ecosystems include the open-source Einstein Toolkit, GRChombo/GRTL codes, and Warp Factory-style metric/energy-condition analysis. This repository should cite and interoperate where appropriate rather than pretend those capabilities were invented here.

## What to build first

**Week-zero goal:** one candidate, one validator, one explanation.

1. Implement the candidate schema.
2. Add Candidate 000001: Minkowski.
3. Validate schema and basic metric properties.
4. Save a machine-readable result.
5. Render a simple human-readable report.
6. Add tests.
7. Make the run deterministic.
8. Document exactly how to reproduce it.

Only then add another benchmark.

## How to contribute

You do not need to be a physicist to contribute. Useful contributions include:

- numerical-relativity expertise;
- differential geometry;
- scientific computing;
- software engineering;
- data engineering;
- reproducibility infrastructure;
- visualization;
- materials science;
- literature curation;
- accessibility and education;
- documentation;
- adversarial review and falsification.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting work.

## Project status

**Experimental / pre-alpha.** The initial repository is architecture and research scaffolding. It is not a validated scientific instrument and contains no evidence of practical spacetime transportation.

## License

Apache License 2.0. See [LICENSE](LICENSE).

## Core principle

> **AI explores. Physics referees. Reproduction decides what survives.**
