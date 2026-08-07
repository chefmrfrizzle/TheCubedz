# Architecture

## Design goal

Build a research operating system with a deterministic scientific core and optional AI assistance around it.

## The five planes

### 1. Evidence plane

Stores literature-derived claims, benchmark definitions, equations, datasets, licenses, citations, and provenance.

Core rule: derived claims retain a path back to their sources.

### 2. Candidate plane

A candidate is immutable once published. A modified candidate receives a new version or identifier.

Minimal candidate object:

```json
{
  "candidate_id": "CANDIDATE-000001",
  "version": "0.1.0",
  "title": "Minkowski baseline",
  "metric": {},
  "coordinates": ["t", "x", "y", "z"],
  "parameters": {},
  "assumptions": [],
  "references": [],
  "provenance": {}
}
```

### 3. Validation plane

Validators consume candidate objects and emit immutable result objects.

```text
candidate + validator version + environment
                    ↓
              deterministic run
                    ↓
result + artifacts + logs + numerical tolerances + hash
```

Validators should be composable. Examples:

- schema validator;
- tensor algebra checks;
- invariant checks;
- numerical constraint evaluator;
- energy-condition evaluator;
- convergence test;
- perturbation runner;
- causal-structure analysis.

### 4. Knowledge plane

The knowledge graph connects:

```text
Paper ──supports/challenges──▶ Claim
Claim ──about───────────────▶ CandidateFamily
Candidate ──instance_of─────▶ CandidateFamily
Candidate ──evaluated_by────▶ Run
Run ──produces──────────────▶ Result
Result ──fails/passes───────▶ Constraint
Result ──reproduced_by──────▶ Reproduction
```

This graph is the project's durable "second brain."

### 5. Search plane

Search policies consume the current evidence map and propose **new experiments**, not new truths.

Possible methods later:

- Bayesian optimization;
- active learning;
- evolutionary search;
- novelty search;
- surrogate modeling;
- constrained optimization;
- graph-based experiment selection.

Every search proposal must preserve which model/policy/version generated it.

## Services

Suggested eventual service boundaries:

```text
web-ui
api-gateway
candidate-registry
experiment-runner
validator-workers
artifact-store
knowledge-graph
search-service
explanation-service
literature-ingestion
reproduction-service
```

Do not begin with all of these as microservices. Start as a modular monolith and separate only when scale or isolation requires it.

## Technology recommendation

### Phase 0

- Python 3.12+
- typed models (Pydantic or equivalent)
- SymPy for small symbolic baseline checks
- NumPy/SciPy for basic numerical scaffolding
- pytest
- JSON/JSONL artifacts
- Docker/OCI reproducibility
- GitHub Actions

### Phase 1+

- PostgreSQL for metadata
- S3-compatible object storage for heavy artifacts
- queue/scheduler for compute jobs
- graph database only if relational + graph projections become insufficient
- React/Next.js frontend for public exploration
- scientific adapters to external numerical-relativity software

## Trust model

### Deterministic computation
High trust when tests, precision, implementation, and reproduction support it.

### Curated evidence
Trust depends on source quality and extraction review.

### AI output
Untrusted proposal until verified.

### User-submitted code
Untrusted executable content; eventually sandbox it.

## Reproducibility envelope

Every run should eventually capture:

```text
candidate hash
source commit
validator version
solver version
dataset snapshot
container/image digest
hardware summary
precision
numerical tolerances
random seeds
command line
stdout/stderr hashes
artifact hashes
wall-clock metadata
```

## What is public?

For a genuinely open-source project, default to public:

- candidate schemas;
- scientific validators;
- benchmark data that licensing allows;
- result schemas;
- documentation;
- test fixtures;
- reproduction tooling;
- search algorithms once ready for release.

If a temporary private research branch exists, never present its outputs as independently reproducible public science until the required methods are released.
