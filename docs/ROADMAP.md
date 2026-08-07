# Roadmap

The machine-readable roadmap is in [`data/roadmap.json`](../data/roadmap.json). This document adds exit criteria and implementation detail.

## Phase 0 — Integrity foundation · complete

- [x] Apache-2.0 public license
- [x] contribution, governance, security, and conduct policies
- [x] scientific claims policy
- [x] candidate/result/claim/event/graph/model-card schemas
- [x] append-only event-ledger contract
- [x] architecture decision records
- [x] public launch acceptance criteria

Exit criterion: scientific status, provenance, corrections, and agent authority are documented before novelty work.

## Phase 1 — One reproducible baseline · live

- [x] Candidate 000001: Minkowski Cartesian baseline
- [x] exact shape, symmetry, determinant, and inverse checks
- [x] scoped analytic flatness implications
- [x] machine-readable result
- [x] beginner and technical reports
- [x] scientific payload digest
- [x] deterministic reproduction command
- [x] test suite
- [ ] independent implementation or solver cross-check
- [ ] outside clean-environment reproduction record

Exit criterion: at least one independent implementation recovers the declared baseline result and discrepancies are resolved or recorded.

## Phase 2 — Benchmark suite · next

- [ ] choose the next smallest established metric through a benchmark-design record
- [ ] add coordinate/convention fixtures
- [ ] define analytic expectations and numerical tolerance policy
- [ ] add a solver-adapter interface
- [ ] implement cross-validator comparison
- [ ] add convergence and failure fixtures where numerical methods begin
- [ ] publish a benchmark passport for each candidate family

Exit criterion: multiple established metrics recover expected properties across at least two implementation paths.

## Phase 3 — Public laboratory · partial

- [x] responsive overview, lab, graph, agents, method, learn, roadmap, and contribute routes
- [x] raw machine-readable artifacts
- [x] artifact-derived explanations
- [x] evidence-graph explorer
- [x] browser convenience cross-check
- [x] build and internal-link fingerprints
- [x] Vercel and GitHub Pages deployment paths
- [ ] reproduction passport submission
- [ ] challenge/falsification issue flow integrated into candidate pages
- [ ] searchable failure atlas
- [ ] contradiction queue
- [ ] accessibility review by outside contributors

Exit criterion: an outside contributor can reproduce, challenge, or improve a candidate through a documented path without maintainer intervention.

## Phase 4 — Transparent search · future

- [ ] frozen synthetic/known benchmark for experiment selection
- [ ] random baseline
- [ ] grid/stratified baseline
- [ ] evolutionary, Bayesian, novelty, and active-learning policies
- [ ] versioned objective and compute-budget contract
- [ ] calibration and information-gain evaluation
- [ ] model cards and rollback
- [ ] working-memory-only proposal queue

Exit criterion: a policy outperforms declared naive baselines on a frozen benchmark without weakening provenance or claim safeguards.

## Phase 5 — Federated reproduction · future

- [ ] authenticated contribution plane
- [ ] reviewed job manifests
- [ ] isolated ephemeral runners
- [ ] no-network-by-default policy
- [ ] resource and output quotas
- [ ] signed result bundles and attestations
- [ ] cross-solver comparison service
- [ ] quality-based contribution records
- [ ] incident response and kill switch

Exit criterion: untrusted community jobs cannot alter canonical state or escape the sandbox, and returned artifacts remain reviewable and reproducible.

## Phase 6 — Novel research · gated

Only after benchmark maturity:

- [ ] novel candidate generation
- [ ] literature novelty review
- [ ] expert mathematical and physical review
- [ ] independent reproduction
- [ ] preprint-quality artifact package
- [ ] external replication

Exit criterion: a novel, narrow claim survives declared falsification tests and independent external scrutiny.

## Explicit non-goals for the alpha

- autonomous scientific publication;
- a universal “works” score;
- public untrusted code execution;
- engagement-based physics rankings;
- financial incentives or speculative markets;
- hundreds of microservices or agents;
- claims of a route to Mars.
