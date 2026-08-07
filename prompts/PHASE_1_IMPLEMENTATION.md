# Copy-Paste Prompt: Implement Phase 1

Act as the lead engineer for this repository. Work directly from the repository's existing documentation and do not rename or brand the project.

Your goal is to complete **Phase 1 — One perfect baseline** from `docs/ROADMAP.md` using Candidate 000001 (Minkowski spacetime).

Requirements:

1. Keep the scientific core deterministic and independent from any LLM.
2. Replace the starter structural validator with proper typed/schema validation while preserving its warning that schema validity is not physical validity.
3. Add small, auditable analytic checks appropriate to the Minkowski baseline. Do not pretend they constitute a general numerical-relativity solver.
4. Define a machine-readable result schema with explicit validator version, candidate hash, timestamps, conventions, checks, status, errors/warnings, and provenance.
5. Generate a deterministic result artifact for Candidate 000001.
6. Add tests for expected baseline behavior and deliberate failure cases.
7. Add one CLI command that a new contributor can run from a fresh clone.
8. Add a human-readable report generator that produces two views from the same verified result: `beginner` and `technical`. Explanations must never change raw result fields.
9. Add GitHub Actions CI for tests and validation.
10. Update documentation with exact reproduction instructions.
11. Do not add databases, queues, vector stores, microservices, authentication, or autonomous training in Phase 1.
12. Keep commits small and conventional, using prefixes documented in `CONTRIBUTING.md`.

Before changing code, write acceptance criteria. After implementation, report exact commands run, tests passed, limitations, and the next smallest milestone.
