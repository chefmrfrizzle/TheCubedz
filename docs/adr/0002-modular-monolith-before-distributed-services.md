# ADR 0002: Modular monolith before distributed services

- Status: Accepted
- Date: 2026-08-07

## Context

The long-term vision includes solvers, agents, graph projections, model training, federated runners, and public interfaces. Premature microservices would create operational complexity before scientific contracts are stable.

## Decision

Begin with one repository, one deterministic Python core, portable JSON contracts, and a statically generated public site. Keep module boundaries explicit so compute workers and data services can be separated later.

## Consequences

- A fresh clone remains understandable.
- CI can reproduce the full V0 release.
- No cloud dependency is required to verify the first result.
- Scaling decisions will be based on measured workloads rather than imagined traffic.
