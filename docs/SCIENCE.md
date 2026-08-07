# Scientific Framing

## Plain-language framing

The project is a search laboratory.

We describe a possible spacetime configuration, ask established mathematics what that configuration implies, test it against known constraints, and store the result. The search system then uses the accumulated map of successes, failures, and uncertainties to decide which candidate regions deserve further computation.

The project is not evidence that spacetime can be engineered for transportation.

## Research hypothesis

> Systematic, reproducible computational search over parameterized spacetime geometries and associated source models may identify, classify, or rule out scientifically interesting regions of solution space more efficiently than isolated manual proposal and analysis alone.

This is a methodological hypothesis. It can be tested without asserting that a traversable wormhole or practical warp configuration exists.

## Core mathematical object

A candidate begins with a metric tensor, coordinates, parameters, assumptions, and optionally a source/matter model.

General relativity connects curvature and stress-energy:

\[
G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4}T_{\mu\nu}.
\]

The software should always distinguish at least four questions:

1. **Definition:** Is the candidate specified unambiguously?
2. **Mathematics:** Does the computation satisfy the equations/constraints being tested?
3. **Physics:** What properties or known theoretical difficulties follow?
4. **Engineering:** Is there any known realizable physical system that approximates the required source?

Passing one layer does not imply passing the next.

## Initial benchmark family

The first phase should use established examples rather than novel generation:

- Minkowski spacetime as the simplest flat baseline.
- Schwarzschild as a foundational curved-vacuum benchmark.
- Additional standard metrics only after the pipeline reproduces expected invariants and numerical results.
- Exotic/transportation-associated metrics should be treated as analysis targets, not engineering designs.

## Candidate evaluation dimensions

A mature candidate report may include:

- schema completeness;
- signature and coordinate conventions;
- determinant / inverse consistency;
- curvature quantities;
- Einstein tensor / stress-energy implications;
- Hamiltonian and momentum constraints when applicable;
- numerical convergence;
- energy-condition analyses;
- geodesic structure;
- horizon/trapped-surface indicators when relevant;
- causal analysis;
- perturbation/stability experiments;
- global assumptions and boundary conditions;
- source-model compatibility;
- uncertainty and numerical error;
- reproduction count.

## Scientific labels

Avoid labels like `WORKS`.

Prefer statements that identify exactly what survived:

- `SCHEMA_VALID`
- `ANALYTIC_CHECKS_PASSED`
- `NUMERICAL_CONVERGENCE_OBSERVED`
- `ENERGY_CONDITION_VIOLATION_DETECTED`
- `STABILITY_UNRESOLVED`
- `INDEPENDENTLY_REPRODUCED`

## Falsification first

For every candidate, store the question:

> What observation, derivation, convergence test, or independent reproduction would cause us to downgrade or reject this claim?

A project that cannot answer this question is accumulating stories, not science.

## External scientific ecosystems

Do not reimplement mature numerical-relativity ecosystems unless a concrete technical reason exists. Design adapters around established tools and record their exact versions/configurations. Candidate metadata should be independent of any single solver so multiple implementations can cross-check the same candidate.
