# ADR 0001: The evidence ledger is the system of record

- Status: Accepted
- Date: 2026-08-07

## Context

The project needs durable scientific memory while models, databases, interfaces, and infrastructure may change.

## Decision

Use an append-only typed event ledger as the source of truth. Treat the evidence graph, search indexes, dashboards, and model datasets as rebuildable projections.

## Consequences

- Corrections append new events rather than rewriting old ones.
- Every status change has provenance.
- Models cannot silently mutate canonical history.
- Rebuilding projections becomes a tested operational requirement.
- Early V0 may use JSON and JSONL before adopting a database.
