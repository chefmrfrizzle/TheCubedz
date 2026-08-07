# Contributing

Thank you for helping test an unusual scientific hypothesis rigorously.

## Before contributing

Read `README.md`, `docs/SCIENCE.md`, and `docs/ARCHITECTURE.md`.

## Contribution types

- `candidate`: a parameterized spacetime/matter/field candidate
- `validator`: a deterministic scientific or numerical check
- `reproduction`: an independent rerun of an existing candidate
- `falsification`: evidence that a result/assumption is wrong or incomplete
- `dataset`: a structured, licensed, citable evidence addition
- `visualization`: a faithful representation of computed data
- `education`: explanations that preserve scientific meaning
- `infrastructure`: tests, CI, storage, schemas, performance, packaging

## Pull-request requirements

Every scientific PR should state:

1. What claim or capability is being added or changed?
2. What source, equation, benchmark, or prior result supports it?
3. What assumptions are being made?
4. How can another contributor reproduce it?
5. What tests were run?
6. What would falsify the result?
7. Does this change a scientific status? If so, why?

AI-assisted contributions are welcome, but the contributor remains responsible for verifying equations, citations, code, and claims.

## Commit style

Use small commits with clear prefixes:

- `docs:` documentation
- `feat:` new capability
- `fix:` bug correction
- `science:` scientific model/validator
- `data:` dataset/schema change
- `test:` tests or benchmarks
- `infra:` tooling/CI
- `refactor:` behavior-preserving restructuring

Example:

```text
science: add Minkowski metric baseline validator
```

## Review philosophy

A reviewer may ask for stronger evidence even when the code works. Scientific correctness and software correctness are separate review dimensions.
