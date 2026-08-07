# Governance

## Purpose

Governance optimizes for reproducibility, scientific integrity, contributor safety, transparent correction, and long-term public accessibility.

## Roles

### Contributor

Proposes code, evidence, candidates, challenges, reproductions, explanations, or governance changes.

### Reviewer

Reviews within demonstrated software, data, scientific, security, accessibility, or community expertise.

### Maintainer

Protects repository health, release quality, contributor workflow, and merge integrity. A maintainer cannot override reproducible evidence by authority alone.

### Scientific reviewer

Reviews equations, conventions, methods, interpretation, benchmark expectations, and claim scope.

### Data steward

Reviews source provenance, licensing, authority tiers, dataset snapshots, corrections, and graph canonicalization.

### Security reviewer

Reviews workflow permissions, dependencies, secrets, untrusted execution, isolation, and incident response.

Early in the project one person may occupy several roles, but the decision records should keep the roles logically separate.

## Decision classes

### Routine

Documentation, tests, accessibility, presentation, and behavior-preserving refactors may be merged by a maintainer after normal review.

### Scientific

Changes to equations, candidate definitions, validator semantics, benchmark expectations, tolerances, result interpretation, or scientific status require:

- explicit scope and assumptions;
- supporting sources or derivation;
- reproducibility commands;
- tests and failure cases;
- a claim-impact note;
- scientific review.

### High-impact

The following should eventually require at least two human approvals:

- candidate/result/claim schema changes;
- canonical scientific status changes;
- model or search-policy promotion;
- public compute execution;
- security-boundary changes;
- license or governance changes;
- deletion or redaction of public evidence.

## Canonical record

The canonical record is the versioned event ledger plus immutable source artifacts—not model memory, a graph database, a website summary, or a popular vote.

Corrections use new events and supersession links. Retractions remain visible.

## Models and prompts

Models and prompts are versioned artifacts. A new model may produce new proposals, but it cannot silently reinterpret historical results or approve its own promotion.

## Conflicts of interest

Contributors and reviewers should disclose financial, employment, authorship, competitive, or personal interests that could materially affect review. Disclosure does not automatically disqualify participation; it informs assignment and interpretation.

## Disputes

1. Identify the exact artifact, claim, method, or conduct issue.
2. Separate scientific disagreement from conduct enforcement.
3. Record competing interpretations and unresolved assumptions.
4. Request an independent review when available.
5. Preserve the history of the decision.
6. Appeal high-impact decisions through a documented governance issue or discussion unless privacy/security requires a private channel.

## Maintainer succession

As the project grows, publish the maintainer list, review domains, inactivity process, and succession path. No private fork or model memory should become the only copy of canonical research.
