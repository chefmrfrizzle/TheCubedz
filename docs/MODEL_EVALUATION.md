# Model and search-policy evaluation

## Purpose

Define what “the system learns” means in measurable terms and prevent self-reinforcing generated errors.

## Candidate learned components

### Retriever

Finds relevant sources, claims, runs, and failures for a candidate.

Metrics:

- recall at k for reviewed relevant evidence;
- citation/source precision;
- contradiction retrieval;
- orphan rate;
- latency and cost.

### Literature classifier

Prioritizes publications or datasets for human review.

Metrics:

- reviewed relevance precision/recall;
- license/provenance error rate;
- duplicate detection;
- calibration.

### Explainer

Changes reading level without changing scientific meaning.

Metrics:

- factual consistency with result fields;
- limitation retention;
- status-language compliance;
- human comprehension;
- accessibility and reading level.

### Anomaly/reproduction ranker

Ranks results that deserve independent reproduction.

Metrics:

- yield of meaningful discrepancies;
- coverage across candidate families;
- false-alarm burden;
- calibration;
- resistance to popularity bias.

### Surrogate model

Approximates expensive validator outputs within a bounded domain.

Metrics:

- error distribution and tail risk;
- uncertainty calibration;
- out-of-distribution detection;
- exact-run escalation rate;
- decision-boundary error.

### Search policy

Chooses the next candidate or validator evaluation.

Metrics:

- information gain per compute unit;
- valid-candidate yield;
- contradiction resolution;
- explored-space coverage;
- redundancy;
- regret against an oracle in synthetic benchmarks;
- reproducibility of proposal rankings.

## Required baselines

Every learned policy is compared with at least:

- random selection;
- simple grid or stratified selection where applicable;
- a transparent hand-written heuristic;
- the current promoted policy.

Without a baseline, “better” has no meaning.

## Dataset contract

Every training or evaluation snapshot records:

```text
snapshot_id
creation_event
source artifacts and hashes
schema versions
license manifest
inclusion/exclusion rules
deduplication method
train/validation/test split IDs
leakage analysis
known coverage gaps
sensitive or restricted fields
```

## Leakage controls

- Candidate families should be grouped across splits when near-duplicates could leak.
- Later corrections and reproductions must not leak into historical evaluation snapshots.
- The model cannot access hidden benchmark answers through retrieval tools.
- Prompt examples derived from evaluation cases are tracked as contamination.
- User telemetry is excluded from physics-label training.

## Promotion gate

A model card must show:

1. intended and prohibited uses;
2. input snapshot and code commit;
3. metrics against all baselines;
4. calibration and subgroup/family performance;
5. robustness and adversarial tests;
6. known failure modes;
7. cost and latency;
8. reproducibility instructions;
9. human reviewer decision;
10. rollback target.

## Online operation

A promoted model may create proposals in working memory. It may not:

- write canonical results;
- change a claim class;
- train continuously on its own output;
- use clicks as physical truth;
- see private evaluation answers;
- suppress contradictory evidence;
- approve its own replacement.

## Monitoring

Monitor:

- input-distribution drift;
- citation/provenance failures;
- calibration drift;
- repeated proposal collapse;
- cost spikes;
- challenge and correction rate;
- differential performance across candidate families;
- any status-language policy violation.

Rollback occurs when safeguards regress even if headline search yield improves.
