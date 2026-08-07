# Roadmap

## Phase 0 — Repository integrity

- [x] Open-source license
- [x] Governance and contribution rules
- [x] Scientific framing
- [x] Candidate schema draft
- [ ] CI
- [ ] formatting/linting
- [ ] release process

## Phase 1 — One perfect baseline

- [ ] Candidate 000001: Minkowski
- [ ] schema validation
- [ ] analytic metric/inverse tests
- [ ] basic invariant checks
- [ ] machine-readable result
- [ ] beginner + technical explanation
- [ ] deterministic reproduction command

Exit criterion: a fresh clone reproduces the same baseline result.

## Phase 2 — Benchmark suite

- [ ] Schwarzschild benchmark
- [ ] additional established metrics
- [ ] solver adapter interface
- [ ] numerical convergence harness
- [ ] cross-solver result comparison

Exit criterion: expected benchmark properties are reproduced within documented tolerances.

## Phase 3 — Public lab

- [ ] candidate explorer
- [ ] result pages
- [ ] "why did this fail?" explanation
- [ ] contribution workflow
- [ ] failure map
- [ ] reproducibility fingerprints

## Phase 4 — Search

- [ ] parameter-space representation
- [ ] random baseline search
- [ ] Bayesian/evolutionary/active-learning experiments
- [ ] frozen benchmark for search quality
- [ ] search-policy versioning

Exit criterion: a learned/search policy outperforms a defined naive baseline on a reproducible benchmark.

## Phase 5 — Distributed science

- [ ] sandboxed community jobs
- [ ] independent reproductions
- [ ] challenge/falsification workflow
- [ ] signed artifacts
- [ ] reputation based on reproduced contribution quality, not popularity

## Phase 6 — Novel research

Only after the earlier gates:
- [ ] novel candidate generation
- [ ] expert scientific review
- [ ] preprint-quality reproducibility packages
- [ ] external replication
