# Architecture

## Design goal

Build a research operating system with a deterministic scientific core, an append-only evidence memory, and optional AI assistance around—not inside—the scientific authority boundary.

## Current V0 modules

```text
candidates/*.json
      │
      ▼
src/research_core/                 deterministic scientific core
      │
      ├── exact matrix operations
      ├── schema validation
      ├── scoped benchmark profile
      └── result/report generation
      │
      ▼
artifacts/results + reports        canonical release artifacts
      │
      ├───────────────┐
      ▼               ▼
data/ledger      data/knowledge-graph.json
      │               │
      └───────┬───────┘
              ▼
web/ + scripts/build_site.mjs      public read-only exploration layer
```

V0 is a modular monolith and static export. This is intentional.

## Six logical planes

### 1. Evidence plane

Stores source-derived claims, benchmark definitions, licenses, citations, and provenance.

Core rule: every derived claim retains a path back to a source location or deterministic artifact.

### 2. Candidate plane

A candidate is a versioned, immutable scientific proposal containing coordinates, conventions, metric/source definition, parameters, assumptions, claims, falsification conditions, references, and provenance.

A modified candidate receives a new version or identifier.

### 3. Validation plane

Validators consume candidate objects and emit immutable result objects.

```text
candidate hash + validator version + declared environment
                         │
                         ▼
                 deterministic run
                         │
                         ▼
checks + assessment + warnings + errors + limitations + digest
```

Validators are scoped and composable. A validator never inherits authority from a different validator merely because both are shown on one page.

### 4. Knowledge plane

The append-only event ledger is the source of truth. The evidence graph is a rebuildable projection connecting questions, sources, claims, candidates, validators, runs, failures, reproductions, corrections, and models.

### 5. Search/learning plane

Models consume frozen, content-addressed snapshots and propose next experiments in working memory.

Potential future methods include random/grid baselines, Bayesian optimization, active learning, evolutionary search, novelty search, surrogate modeling, and graph-based experiment selection.

Every proposal records policy ID, version, input snapshot, objective, compute budget, uncertainty, and baseline comparison.

### 6. Public plane

The website reads committed artifacts and offers accessible explanations, graph exploration, reproduction commands, and contribution paths. It cannot write canonical state or execute untrusted submissions.

## Trust model

| Source | Default authority |
|---|---|
| Exact deterministic result with tests | High within declared scope |
| Independently reproduced result | Higher, subject to independence level and discrepancies |
| Curated primary/authoritative evidence | Depends on source and extraction review |
| Agent/model output | Working-memory proposal only |
| Browser convenience calculation | Noncanonical demonstration |
| User-submitted executable | Untrusted; not run in V0 |
| Popularity or engagement | No scientific authority |

## Reproducibility envelope

A mature run should capture:

```text
candidate ID, version, and hash
source commit
validator and solver versions
dataset snapshot
container/image digest
hardware and architecture
precision and numerical tolerances
random seeds
command line
stdout/stderr hashes
artifact hashes
wall-clock metadata
```

The current baseline captures the subset relevant to its exact deterministic profile.

## Current technology

- Python 3.12+;
- `jsonschema` and typed JSON contracts;
- exact rational arithmetic using the standard library;
- pytest;
- JSON/JSONL/Markdown artifacts;
- dependency-free static HTML/CSS/JavaScript;
- Node-based deterministic site build and validation;
- GitHub Actions, Vercel, and GitHub Pages deployment paths.

## Future service boundaries

Do not begin with these as microservices. Extract only after measured demand or security isolation requires it:

```text
contribution-api
candidate-registry
experiment-scheduler
sandboxed-validator-workers
artifact-store
evidence-ledger
graph/search-projection
snapshot-builder
model-training-and-evaluation
explanation-service
public-export-builder
```

See [Scale architecture](SCALE_ARCHITECTURE.md) and [ADR 0002](adr/0002-modular-monolith-before-distributed-services.md).

## External scientific ecosystems

The project should integrate established numerical-relativity and scientific-computing systems through versioned adapters rather than pretending to replace them. Candidate and result contracts should remain solver-independent enough to enable cross-implementation comparison.

## Public/open default

Default to public when licensing and security allow:

- schemas;
- validators;
- benchmark definitions;
- results and failures;
- reproducibility tooling;
- dataset manifests;
- model cards and evaluation summaries;
- prompts and authority policies;
- static public exports.

A temporary private research branch cannot support a public reproducibility claim until the required methods and artifacts are released.
