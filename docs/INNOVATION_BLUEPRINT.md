# Innovation blueprint

This document preserves ambitious product and research ideas while marking what is implemented, what should come next, and what must remain gated.

## Portfolio rule

An idea earns implementation priority when it improves at least one of:

- reproducibility;
- falsifiability;
- information gain;
- scientific accessibility;
- provenance;
- cross-validator agreement;
- security;
- contributor effectiveness.

Excitement alone is not a priority score.

## Implemented now

### Multi-level explanation compiler

One result artifact drives beginner and technical reports. Vocabulary may change; status and limitations may not.

### Scientific payload fingerprint

The digest excludes runtime noise and covers the candidate identity, validator, checks, assessment, warnings, errors, and limitations.

### Evidence graph

Questions, hypotheses, challenges, candidate families, candidates, validators, runs, claims, reproduction queues, and search policies are typed nodes with explicit relationships.

### Browser cross-check

Visitors can recompute basic matrix properties locally. The UI explicitly distinguishes this from the canonical Python artifact.

### Reusable static export

The full public laboratory can be forked and deployed without a backend or private service.

## Build next

### Independent baseline validator

Implement Candidate 000001 through a second code path or established symbolic system. Cross-implementation agreement is more valuable than repeatedly running the same code.

### Reproduction passport

A machine-readable record containing contributor, environment, implementation independence, tolerance, result comparison, discrepancies, and signed artifact hashes.

### Failure atlas

Index failures by candidate family, validator, assumption, parameter region, numerical resolution, and status. Preserve negative results as first-class searchable objects.

### Contradiction queue

Surface claims or runs that cannot both be true under the same assumptions. Assign a review state and resolution record.

### Benchmark passport

For each established metric, publish expected properties, references, accepted coordinate forms, validator coverage, cross-solver results, and known failure tests.

### Challenge-first pull requests

Allow contributors to submit a falsification test before writing a candidate implementation. This prevents large code changes around an untestable idea.

## Build after benchmark maturity

### Uncertainty topology

Visualize tested, rejected, unresolved, contradictory, under-resolved, and untouched regions separately. Avoid a single “promise score.”

### Transparent search tournaments

Run random, grid, evolutionary, Bayesian, novelty, and active-learning policies against the same frozen benchmark, compute budget, and scoring contract.

### Counterfactual navigator

For a failed candidate, estimate the smallest parameter or assumption changes that would alter a specific validator outcome. Label approximations and never imply engineering feasibility.

### Surrogate-model uncertainty

Use bounded surrogate models to approximate expensive validator outputs while showing epistemic uncertainty and forcing exact runs near decision boundaries.

### Research quests

Turn bounded gaps into contribution tasks: reproduce a run, resolve a contradiction, add a test, translate an explanation, or validate an external solver adapter.

### Quality-based contributor reputation

Credit reproducible artifacts, resolved contradictions, accepted challenges, and corrections. Do not reward popularity, speculative certainty, or compute volume alone.

## Build only with strong security capacity

### Federated compute

Contributors run approved jobs in isolated environments and return signed manifests, logs, and artifacts. The central system verifies output structure and provenance before review.

### Public candidate submission

Requires authentication, moderation, input schemas, abuse prevention, license declarations, and no direct execution in the website environment.

### Sandboxed solver marketplace

Requires microVM/container isolation, network denial, resource quotas, syscall policy, artifact scanning, deterministic images, kill switches, and funding controls.

## Research-frontier ideas

### Geometry representation learning

Learn embeddings that preserve scientifically meaningful similarity between candidate configurations, failure signatures, and validator outputs.

### Active falsification

Choose experiments most likely to discriminate between competing claims rather than merely optimize a transportation-related objective.

### Proof-carrying candidates

Require candidates to include machine-checkable derivations or invariant certificates where possible.

### Causal provenance queries

Ask not only “what supports this claim?” but “which assumptions and transformations were necessary for this status?”

### Domain forks

Reuse the protocol outside spacetime research:

```text
candidate → validator → artifact → challenge → graph → frozen snapshot → search policy
```

Potential domains include materials discovery, mathematical conjectures, engineering design spaces, climate-model intercomparison, and robotics policy evaluation. Each fork needs domain-specific validators and governance; the protocol alone does not transfer scientific authority.

## Explicitly not planned for V0

- tokens or financial incentives;
- prediction markets;
- autonomous publication of scientific claims;
- engagement-driven truth scores;
- hidden proprietary validators behind public claims;
- unreviewed user code execution;
- a universal “probability this reaches Mars” meter;
- hundreds of agents before one benchmark is excellent.
