# Evidence graph

## Why a graph?

Scientific research is not a pile of documents. It is a network of questions, assumptions, definitions, calculations, claims, objections, corrections, and reproductions. A graph makes those relationships queryable without flattening them into one misleading score.

## Core node types

- `ResearchQuestion`
- `Hypothesis`
- `Challenge`
- `CandidateFamily`
- `Candidate`
- `Validator`
- `Run`
- `Claim`
- `ReproductionQueue` and `Reproduction`
- `Source`
- `Correction`
- `SearchPolicy`

## Core relationships

- `FRAMES`
- `MOTIVATES`
- `INSTANCE_OF`
- `EVALUATES`
- `USES`
- `SUPPORTED_BY`
- `CHALLENGES`
- `REQUESTS_REPRODUCTION_OF`
- `REPRODUCES`
- `CONTRADICTS`
- `SUPERSEDES`
- `WILL_TEST`

## Authority rule

Edges carry authority just as nodes do. A working-memory link such as “an agent thinks paper X supports claim Y” is not equivalent to a reviewed canonical link. Interfaces must visually separate them.

## Graph questions the system should answer

- Which exact result supports this claim?
- Which validator and source commit produced it?
- Has anyone reproduced it independently?
- Which assumptions remain untested?
- What failed, and where is the failure artifact?
- Which claims were superseded or retracted?
- Which candidate regions are untested rather than merely unpopular?
- What snapshot and policy proposed the next experiment?

## V0

`data/knowledge-graph.json` is the first static snapshot. It is validated in CI and rendered by the public website. A production database is intentionally deferred until the contracts and governance are stable.
