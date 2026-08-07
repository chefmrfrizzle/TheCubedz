# Data governance

## Collection principle

Collect the minimum information needed to reproduce research and improve the instrument. Public scientific status must not depend on personal profiling, hidden telemetry, or engagement optimization.

## Required provenance

Every canonical object should record:

- creator or generating system;
- creation time;
- source paths or citations;
- license and reuse restrictions;
- schema version;
- content hash;
- review state;
- supersession or correction links.

## User activity

V0 has no account system or analytics dependency. Later telemetry must be opt-in or privacy-preserving, minimized, retention-limited, and stored outside scientific memory. Telemetry may improve explanations, accessibility, search, and performance. It cannot promote a claim or train a physics judge.

## Papers and datasets

Do not indiscriminately scrape copyrighted papers into a training corpus. Store metadata, citations, narrow licensed extracts, structured claims, and links. Track the license and permitted use for every snapshot.

## Model training

A training snapshot must include:

- immutable snapshot ID and digest;
- included and excluded object IDs;
- license manifest;
- deduplication method;
- train, validation, and frozen test assignments;
- known contamination risks;
- benchmark version;
- deletion and correction policy.

## Retention

Canonical corrections and retractions remain permanent. Personal data and product telemetry should have separate, shorter retention rules. Secrets, credentials, private correspondence, and sensitive personal information do not belong in the public ledger.
