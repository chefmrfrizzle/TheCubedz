# Contributing

Thank you for helping test an unusual scientific hypothesis rigorously.

## Start here

Read:

1. [README.md](README.md)
2. [Scientific claims policy](docs/SCIENTIFIC_CLAIMS_POLICY.md)
3. [Architecture](docs/ARCHITECTURE.md)
4. [Code of Conduct](CODE_OF_CONDUCT.md)

For agent-assisted work, also read [Agent operating system](docs/AGENT_OPERATING_SYSTEM.md).

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --no-build-isolation -e '.[dev]'
npm ci
npm run check
```

Do not open a pull request until `npm run check` passes or the PR clearly documents a pre-existing failure.

## Contribution types

- `candidate`: a schema-conforming spacetime/matter/field candidate;
- `validator`: a deterministic mathematical, numerical, or scientific check;
- `benchmark`: an established case with expected properties and failure fixtures;
- `reproduction`: a clean-environment or independent-implementation comparison;
- `challenge`: a hidden assumption, contradiction, counterexample, or failure test;
- `evidence`: a licensed, citable, location-specific source addition;
- `data`: schema, ledger, graph, or snapshot work;
- `visualization`: a faithful view of committed data;
- `education`: explanations that preserve status, uncertainty, provenance, and limitations;
- `security`: threat model, workflow, sandbox, or dependency hardening;
- `infrastructure`: tests, CI, static build, packaging, or performance.

## Choose the authority tier

Every contribution should identify its authority tier:

- **A — Canonical science:** reviewed candidate/result/evidence/reproduction/correction records;
- **B — Working research:** hypotheses, drafts, unresolved extractions, agent proposals, and challenge queues;
- **C — Product telemetry:** interface and comprehension signals that cannot alter physics status.

When uncertain, submit to Tier B.

## Pull-request requirements

Every PR should answer:

1. What bounded problem does this solve?
2. Which files, schemas, candidates, claims, or routes change?
3. What remains explicitly unchanged?
4. Which sources, equations, benchmarks, or prior results support it?
5. Which assumptions and conventions apply?
6. How can another contributor reproduce the result?
7. Which positive, negative, boundary, and regression tests were run?
8. What would falsify, downgrade, or reject the contribution?
9. Does any scientific status change? Why is the evidence sufficient?
10. Was AI used, and how were generated code, equations, citations, and claims reviewed?

## Scientific contribution rules

- A candidate draft cannot label itself valid.
- A validator may claim only what it implements.
- Numerical output includes method, precision/tolerance, convergence evidence where relevant, and environment.
- Coordinate, signature, unit, and cosmological-constant conventions are explicit.
- Mathematical consistency, physical admissibility, stability, causality, realizability, reproduction, and experiment remain separate.
- Unknown remains unknown.
- Negative results stay discoverable.
- A correction supersedes; it does not erase history.
- Repeated runs of the same implementation are not independent scientific reproduction.
- AI output is a proposal until an external evidence gate validates it.

## Data and citation rules

- Prefer primary or authoritative sources.
- Record an exact page, equation, section, table, figure, or dataset location when possible.
- Do not paste copyrighted papers or large excerpts into the repository.
- Record the source license and redistribution restrictions.
- Do not invent or autocomplete citations.
- Contradictory sources remain linked and visible until reviewed.

## Website contribution rules

The public site may explain and visualize committed artifacts. It may not:

- hide limitations;
- upgrade scientific status;
- represent browser convenience checks as canonical results;
- execute untrusted submitted code;
- add sensational language;
- introduce a brand name without a separate project decision.

Validate website changes at desktop and mobile sizes, with keyboard navigation and browser console inspection.

## Commit style

Use small Conventional Commits:

```text
docs: clarify independent reproduction levels
feat(web): add accessible graph filters
science: add second baseline validator
fix(data): preserve superseded claim lineage
test: add non-degenerate metric failure fixture
infra: add release contract workflow
security: reduce workflow permissions
```

Do not combine unrelated refactors, scientific changes, and generated artifact updates in one commit.

## Review model

Software correctness and scientific correctness are separate review dimensions.

A reviewer may approve code quality while requesting stronger scientific evidence. Changes to schemas, validator semantics, scientific status, model promotion, security boundaries, and governance should receive explicit specialist review as the community grows.

## First recommended contribution

Reproduce Candidate 000001 in a clean environment and report whether the scientific payload digest matches. Use the reproduction issue form and [federated reproduction protocol](docs/FEDERATED_REPRODUCTION.md).
