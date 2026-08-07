# Agent system

## Principle

Agents are specialized research workers. They may propose, organize, invoke approved deterministic tools, critique, and explain. They do not receive scientific authority simply because they are autonomous or agree with one another.

The current public contracts live in [`data/agents.json`](../data/agents.json). Copy-pasteable role prompts live in [`prompts/`](../prompts/).

## Current nine-role graph

```text
                       Orchestrator
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
  Literature agent   Candidate agent    Skeptic agent
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                       Math/GR agent
                            │
                            ▼
                       Result ledger
                            │
            ┌───────────────┼────────────────┐
            ▼               ▼                ▼
    Reproduction agent  Explainer agent  Graph curator
                                              │
                                              ▼
                                      Search-policy agent
                                              │
                                              ▼
                                      next proposal only
```

## Current roles

### Orchestrator

Routes bounded tasks, checks authority and output schemas, and records every handoff. It cannot promote scientific status.

### Literature agent

Finds sources and proposes narrow claim extracts with locations, licenses, and contradictions. A summary is not proof.

### Candidate agent

Transforms a hypothesis into a schema-conforming draft with assumptions and falsification criteria. It cannot mark the candidate valid.

### Math/GR agent

Prepares and invokes approved deterministic calculations, preserves conventions, and reports uncertainty. Solver output—not agent prose—is the computation.

### Skeptic agent

Searches for hidden assumptions, coordinate mistakes, weak convergence, prior art, citation gaps, and interpretation stronger than the result.

### Reproduction agent

Runs pinned artifacts in a clean environment, declares implementation independence, and records mismatches rather than smoothing them away.

### Explainer agent

Creates multiple reading levels from the same verified artifact while retaining status, provenance, and limitations.

### Graph curator

Proposes links, deduplication, supersession, snapshots, and orphan detection. Canonical merges require human review.

### Search-policy agent

Consumes a frozen snapshot and proposes next experiments under a transparent objective and compute budget. It is not yet implemented or promoted.

## Future specialist roles

Energy-condition, stability, causality, geodesic, numerical-convergence, materials/realizability, security, and release agents may be introduced as bounded roles once corresponding deterministic methods and review capacity exist.

Do not create an agent merely to create the appearance of sophistication.

## Permission pattern

| Role | Read evidence | Write working memory | Run approved tool | Change canonical status | Train/promote itself |
|---|---:|---:|---:|---:|---:|
| Literature | Yes | Yes | Source tools | No | No |
| Candidate | Yes | Yes | No | No | No |
| Math/GR | Yes | Yes | Yes | No | No |
| Skeptic | Yes | Yes | Optional tests | No | No |
| Reproduction | Yes | Yes | Yes | No | No |
| Explainer | Verified artifacts | Yes | No | No | No |
| Curator | Yes | Yes | Snapshot tools | Propose only | No |
| Search policy | Frozen snapshot | Yes | No | No | No |
| Training pipeline | Named snapshot only | Model registry | Yes | No | No |

## Anti-loop rule

An agent-generated statement may not become training truth merely because another agent repeats, summarizes, votes for, or embeds it. Promotion into canonical data requires a deterministic result, properly sourced evidence, a reviewed annotation, or an explicit reproduction/correction event.

See [Agent operating system](AGENT_OPERATING_SYSTEM.md).
