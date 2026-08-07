# The second brain

## Plain-language model

The project should not behave like an AI that reads the internet, believes itself, and continuously retrains. The durable “brain” is a public research memory:

1. a versioned candidate,
2. a deterministic run,
3. an explicit result,
4. a claim narrower than the result,
5. challenges and reproductions,
6. permanent corrections,
7. a graph connecting them.

A model may study a frozen copy of that memory and suggest the next experiment. It cannot turn its suggestion into scientific truth.

## Technical model

The system of record is an append-only event ledger. A versioned evidence graph is a rebuildable projection of that ledger. Models are disposable consumers of content-addressed snapshots.

```text
sources / candidates / runs / challenges / reproductions / telemetry
                              │
                              ▼
                     schema + provenance gates
                              │
                              ▼
                     append-only event ledger
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
        evidence graph               dataset snapshot
                │                           │
                │                           ▼
                │                  offline model training
                │                           │
                │                           ▼
                │                 frozen benchmark suite
                │                           │
                └──────────────┬────────────┘
                               ▼
                         human promotion
                               │
                               ▼
                    next-experiment proposal
                               │
                               └── returns to working memory
```

## Three trust domains

### A. Canonical science

Versioned candidates, validators, result artifacts, reviewed evidence, reproductions, corrections, and retractions. Only explicit evidence gates may change scientific status.

### B. Working research

Hypotheses, paper extractions, agent suggestions, candidate drafts, unresolved anomalies, and challenge queues. These objects guide investigation but are not established facts.

### C. Product telemetry

Voluntary clarity ratings, failed searches, explanation preferences, interface friction, and performance data. These signals may improve presentation and navigation. They must never determine whether physics is correct.

## Learning without self-deception

A model promotion requires:

- a named, immutable training snapshot;
- licenses and exclusions;
- leakage-resistant train/evaluation splits;
- a naive baseline and current champion;
- calibration, regression, cost, and reproducibility tests;
- a model card;
- human approval;
- a rollback target.

No model trains directly on live public clicks. No model trains on its own unreviewed claims. No model is allowed to rewrite history.
