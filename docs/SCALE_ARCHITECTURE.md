# Scale architecture

## Goal

Allow a global community to submit evidence, challenges, reproductions, and eventually bounded compute without giving any single model, worker, or interface authority over scientific truth.

## Scaling principle

Scale the immutable contracts first. Scale infrastructure only after measured demand.

```text
portable schemas + content hashes + event lineage
                       │
                       ▼
              modular monolith (V0–V1)
                       │
          measured bottleneck or isolation need
                       │
                       ▼
             explicit service extraction
```

## Logical planes

### Public read plane

- static export and CDN;
- candidate/result/claim pages;
- graph queries;
- raw artifact downloads;
- documentation and educational views.

This plane can scale globally without write credentials.

### Contribution plane

- authenticated submissions;
- schema and license preflight;
- moderation queue;
- issue/PR linkage;
- challenge and reproduction records.

No submitted executable reaches the compute plane automatically.

### Evidence plane

- append-only event ledger;
- content-addressed artifact storage;
- relational metadata and graph projection;
- source, license, provenance, correction, and retraction records.

### Compute plane

- reviewed job manifests;
- isolated ephemeral workers;
- no network by default;
- resource quotas;
- deterministic images;
- signed outputs and attestations;
- quarantine before canonical review.

### Learning plane

- frozen dataset snapshots;
- train/evaluation separation;
- model registry and cards;
- offline training;
- benchmark service;
- promotion and rollback workflow.

### Governance plane

- role and permission policy;
- human review queues;
- audit log;
- dispute and correction process;
- release and incident management.

## Event model

Every meaningful change becomes a typed event:

```text
SOURCE_ADDED
CLAIM_EXTRACTED
CANDIDATE_PROPOSED
VALIDATION_STARTED
RESULT_RECORDED
CHALLENGE_OPENED
REPRODUCTION_RECORDED
CLAIM_SUPERSEDED
CLAIM_RETRACTED
DATASET_SNAPSHOTTED
MODEL_EVALUATED
MODEL_PROMOTED
MODEL_ROLLED_BACK
```

The graph, search index, dashboards, and training datasets are projections. They can be rebuilt from the ledger plus immutable artifacts.

## Identity and addressing

Use stable human-readable IDs plus content hashes:

```text
CANDIDATE-000001@1.0.0
RESULT-CANDIDATE-000001-...
sha256:...
```

Human-readable IDs support discussion. Content hashes support integrity. Versions support correction without erasure.

## Storage path

### V0

- Git for reviewed source and small canonical artifacts;
- JSON/JSONL/Markdown;
- static site export.

### V1

- PostgreSQL for metadata, workflow, and permissions;
- S3-compatible object storage for large artifacts;
- Git remains the public release record;
- graph remains a projection, initially relational.

### V2

- event stream for high-volume run and reproduction events;
- partitioned artifact storage;
- read replicas and global CDN;
- specialized graph/search system only when query evidence justifies it.

## Global contribution path

```text
submit metadata
      ↓
license/provenance/schema preflight
      ↓
working-memory record
      ↓
human or trusted-review approval
      ↓
optional isolated compute job
      ↓
quarantined result bundle
      ↓
verification + challenge
      ↓
canonical event
      ↓
public static/read projection
```

## Multi-region consistency

Scientific status changes require strong consistency and a single ordered ledger. Public read projections may be eventually consistent because they are derived views.

Never resolve conflicting scientific status through “last write wins.” Conflicts become explicit challenge or supersession events.

## Cost controls

- static public reads;
- content deduplication;
- bounded result sizes;
- cost estimates before scheduling;
- per-project and per-contributor quotas;
- cheap validators before expensive solvers;
- surrogate models only as triage, never final authority;
- cache exact repeated computations by content hash;
- sponsor-funded queues separated from core integrity.

## Extraction triggers

Create a service boundary only when one of these is observed:

- untrusted compute requires isolation from the application;
- job duration exceeds request lifetimes;
- artifact size exceeds Git practicality;
- contribution moderation needs role-based access;
- graph/query load becomes a measured bottleneck;
- model training requires restricted snapshots;
- data residency or legal obligations require separation.

## Anti-patterns

- microservices before stable schemas;
- a graph database as the source of truth;
- allowing model memory to replace event history;
- global write access to scientific status;
- compute workers with deployment credentials;
- public jobs with unrestricted network access;
- hidden proprietary validation behind public claims;
- engagement ranking presented as scientific merit.
