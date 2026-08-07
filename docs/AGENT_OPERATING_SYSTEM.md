# Agent operating system

## Goal

Use multiple specialized agents to accelerate research and engineering without allowing generated prose to become scientific authority.

## Core rule

> An agent may propose an artifact only inside its declared authority. A different gate decides whether that artifact advances.

## Handoff envelope

Every agent task should include:

```yaml
task_id: TASK-...
role: AGENT-...
objective: one bounded outcome
inputs:
  - content-addressed artifact or explicit source
allowed_tools:
  - named tools only
write_scope:
  - working-memory paths only
forbidden_actions:
  - status promotion
  - citation invention
  - hidden network execution
required_outputs:
  - schema-conforming artifact
  - assumptions
  - limitations
  - validation commands
  - unresolved questions
definition_of_done:
  - exact measurable checks
```

## Authority matrix

| Artifact | Draft | Deterministically compute | Challenge | Recommend status | Approve status |
|---|---|---|---|---|---|
| Literature evidence | Literature agent | N/A | Skeptic/curator | Curator | Human reviewer |
| Candidate | Candidate/search agent | N/A | Skeptic | Science reviewer | Human reviewer |
| Result | Math/solver adapter | Approved tool | Skeptic/reproduction | Reproduction board | Human reviewer |
| Explanation | Explainer | N/A | Contributor | Documentation reviewer | Human reviewer |
| Dataset snapshot | Curator | Snapshot builder | Data-quality agent | Data steward | Human maintainer |
| Search model | Training pipeline | Training runner | Evaluation agent | Model review board | Human maintainer |

No single agent occupies both proposal and approval columns.

## Agent lifecycle

```text
brief
  ↓
input validation
  ↓
bounded execution
  ↓
typed artifact
  ↓
deterministic checks
  ↓
adversarial review
  ↓
human decision
  ↓
ledger event
```

## Recommended agent roster

### Orchestrator

Routes tasks, validates envelopes, records provenance, and stops unauthorized handoffs.

### Literature agent

Finds primary sources, records exact locations, identifies license constraints, and proposes claim extracts.

### Candidate agent

Converts a human or search-policy hypothesis into a schema-conforming draft with assumptions and falsification criteria.

### Math/GR agent

Prepares approved symbolic or numerical jobs, records conventions, and returns raw outputs. It does not replace solver output with a prose conclusion.

### Skeptic agent

Searches for coordinate mistakes, missing assumptions, insufficient resolution, known counterexamples, citation gaps, and interpretation stronger than the result.

### Reproduction agent

Runs pinned inputs in a clean environment, records environment differences, and compares scientific payloads.

### Explainer agent

Produces beginner, intermediate, and technical explanations from the same verified object without hiding limitations.

### Graph curator

Proposes deduplication, links, supersession, and orphan detection while retaining complete lineage.

### Search-policy agent

Consumes a frozen graph/dataset snapshot and ranks next experiments under a declared objective and compute budget.

### Security review agent

Audits dependency changes, workflow permissions, input boundaries, untrusted execution, and release headers.

### Release agent

Runs the release checklist, compares generated artifacts, prepares a changelog, and refuses release when claims or hashes drift.

## Anti-collusion and anti-loop rules

1. Agent A repeating Agent B does not create independent evidence.
2. Two agents using the same source and implementation do not count as independent reproduction.
3. An orchestrator cannot silently edit a specialist output.
4. Generated candidate novelty is not a score until checked against literature and benchmarks.
5. Model outputs remain working memory until an external evidence gate promotes them.
6. Every agent result records model, prompt version, tools, input snapshot, and output hash.

## Human review board

Early in the project one maintainer may perform several human roles, but the roles remain logically separate:

- scientific scope reviewer;
- software/reproducibility reviewer;
- data/provenance reviewer;
- security reviewer;
- release approver.

As the community grows, require two-person review for changes to candidate/result schemas, scientific status, model promotion, security boundaries, and governance.
