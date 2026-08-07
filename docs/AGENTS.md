# Agent System

## Principle

Agents are specialized research workers. They may propose, organize, calculate through approved tools, critique, and explain. They do not receive authority simply because they are autonomous.

## Agent graph

```text
                     ┌───────────────┐
                     │ Orchestrator  │
                     └───────┬───────┘
         ┌───────────────────┼───────────────────────┐
         ▼                   ▼                       ▼
 Literature Agent      Candidate Agent          Skeptic Agent
         │                   │                       │
         ▼                   ▼                       ▼
 Evidence Queue       Candidate Queue          Challenge Queue
         └───────────────────┼───────────────────────┘
                             ▼
                     Validator Pipeline
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
    Math Agent          Stability Agent       Causality Agent
        └────────────────────┼────────────────────┘
                             ▼
                       Result Ledger
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
       Reproduction      Explainer        Search Agent
          Agent            Agent              │
             └───────────────┼────────────────┘
                             ▼
                        Next experiment
```

## Recommended agents

### Orchestrator
Routes tasks, enforces schemas, and prevents agents from bypassing validation gates.

### Literature Agent
Finds relevant work and produces structured candidate claims with citations, not free-floating summaries.

Output example:

```json
{
  "claim": "...",
  "source": "...",
  "location": "equation/section/page",
  "confidence": "extracted_not_verified",
  "relevance": ["energy_conditions"]
}
```

### Candidate Agent
Transforms a human hypothesis or search-policy proposal into a candidate draft. It cannot mark the draft scientifically valid.

### Math/GR Agent
Builds calculation plans and invokes deterministic math/scientific tooling. It must report conventions explicitly.

### Energy-Conditions Agent
Produces condition-specific analyses from computed tensors/metrics and records sampling/assumptions.

### Stability Agent
Defines controlled perturbations, convergence criteria, and stability experiments.

### Causality Agent
Checks for causal questions requiring formal analysis and prevents a transportation score from hiding causal pathologies.

### Materials/Realizability Agent
Searches structured materials/field evidence for compatibility with required physical properties. Its output is a compatibility assessment, not a fabrication recipe.

### Skeptic Agent
Attempts to break the candidate. It asks:
- Which assumption is doing most of the work?
- Which coordinate/convention mistake could create a false result?
- Is the numerical resolution sufficient?
- Is the result already known?
- Is a claimed physical interpretation stronger than the computation supports?

### Reproduction Agent
Runs the candidate in a clean environment from pinned artifacts. It compares hashes and numerical tolerances.

### Explainer Agent
Takes only verified result objects plus approved evidence and generates:
- beginner explanation;
- intermediate explanation;
- technical explanation.

### Search Agent
Consumes the explored map and proposes the next candidate/experiment to maximize scientific information or a transparent optimization objective.

### Curator Agent
Deduplicates and proposes canonicalization of evidence. Human approval is required for high-impact status changes.

## Agent permissions

Use least privilege.

Example:

| Agent | Read evidence | Write working memory | Run solver | Change canonical status | Train model |
|---|---:|---:|---:|---:|---:|
| Literature | Yes | Yes | No | No | No |
| Candidate | Yes | Yes | No | No | No |
| Math/GR | Yes | Yes | Yes | No | No |
| Skeptic | Yes | Yes | Optional tests | No | No |
| Reproduction | Yes | Yes | Yes | No | No |
| Curator | Yes | Yes | No | Propose only | No |
| Search | Yes | Yes | No | No | No |
| Training pipeline | Snapshot only | No | No | No | Yes |

## Anti-loop rule

An agent-generated statement may not become training truth merely because another agent repeats it. Promotion into canonical scientific data requires a deterministic result, a properly sourced evidence item, or an explicit reviewed annotation.
