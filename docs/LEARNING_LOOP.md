# Learning Loop / "Second Brain"

## The beginner explanation

Think of the system as having a notebook and a student.

The **notebook** contains everything that actually happened: candidates, calculations, sources, failures, reproductions, and corrections.

The **student** is the current AI/search model. It reads the notebook and tries to choose a smarter experiment next time.

If the student gets replaced, the notebook remains.

That is the safest definition of a "second brain."

## Why not continuously retrain on every user action?

Because engagement is not scientific evidence. A popular candidate can be wrong. A misunderstood explanation can receive many clicks. A malicious contributor can poison data. And a model trained on its own unverified generations can amplify its errors.

Therefore the online loop collects **events**, while learning happens in controlled, versioned training cycles.

## Three memory tiers

### Tier A — Canonical scientific record

High-integrity, versioned, reviewable.

Contains:
- candidate definitions;
- deterministic run results;
- reproductions;
- validated literature claims;
- corrections/retractions;
- exact provenance.

### Tier B — Research working memory

Useful but not canonical.

Contains:
- hypotheses;
- agent suggestions;
- unresolved extracted claims;
- proposed links;
- experiment queues.

### Tier C — Product telemetry

Contains:
- explanation-level selections;
- failed searches;
- UI friction;
- feature usage;
- voluntary ratings.

Telemetry can improve UX and experiment prioritization but cannot upgrade scientific truth.

## Learning pipeline

```text
1. Ingest
   papers / datasets / candidate submissions / reproductions / telemetry

2. Normalize
   convert to typed, provenance-carrying events

3. Validate
   schema + source + computation + duplication checks

4. Classify
   canonical / working-memory / telemetry

5. Snapshot
   create immutable dataset version

6. Train offline
   search surrogate / ranker / retrieval model / explainer

7. Evaluate
   frozen benchmark suite + regression tests + calibration

8. Review
   human approval for promotion

9. Deploy
   model/policy receives a version and changelog

10. Observe
   new proposals and experiments become new events
```

## What can learn?

Different components learn different things:

- **Retriever:** which evidence is relevant to a candidate.
- **Explainer:** which explanation style helps a user understand a verified result.
- **Surrogate model:** approximate expensive simulation outputs in bounded domains.
- **Search policy:** which candidate region is most informative to evaluate next.
- **Anomaly detector:** which results deserve independent reproduction.
- **Literature classifier:** which new publications may change known claims.

## What must not be learned from popularity?

- whether an equation is correct;
- whether an energy condition is satisfied;
- whether a numerical solution converged;
- whether a result is experimentally demonstrated;
- whether a candidate is physically realizable.

Those require mathematics, computation, evidence, or experiment.

## Training record

Every trained artifact should record:

```text
model_id
model_family
training_code_commit
dataset_snapshot_id
hyperparameters
seed
benchmark_results
known_failure_modes
approval
created_at
```

## Promotion gate

A new model is promoted only if it beats or matches the prior model on frozen benchmarks **without weakening scientific safeguards**.

A model that generates more exciting candidates but more false claims is worse.
