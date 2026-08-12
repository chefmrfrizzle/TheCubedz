# Candidate 000003 external review prompt

Copy this prompt only after replacing `<EXACT_PR_HEAD>` with the current 40-character PR head.

---

Act as an independent general-relativity and scientific-software reviewer. Review TheCubedz Candidate 000003 at exactly:

- Repository: `https://github.com/chefmrfrizzle/TheCubedz`
- Commit: `<EXACT_PR_HEAD>`
- Candidate: `CANDIDATE-000003@1.0.0`
- Passport: `PASSPORT-000003@1.0.0`
- Published expected digest: `sha256:d2b3f4a2ad15a7ade137e4aaf4166bdefab3ff33a3a2a27e5ca232c5bfb43458`

Do not use the published result or EinsteinPy artifact as proof. Start from a clean clone. Record your full name, relevant qualification or public research record, affiliation if any, stable identity link if available, conflicts of interest, OS, architecture, Git commit, Python and solver versions, and every command.

Independently derive the Schwarzschild exterior metric properties in the declared `-+++` signature and Riemann/Ricci conventions. Verify the domain `M > 0`, `r > 2M`, `0 < theta < pi`, the excluded horizon and coordinate axes, metric, inverse, determinant, complete nonzero Christoffel set, representative Riemann components, Ricci tensor, Ricci scalar, Einstein tensor, and Kretschmann scalar. State any convention transformations explicitly.

Prefer a separately controlled R3 implementation or solver that does not import `research_core`. Test at least these failures:

1. change the `g_tt` mass factor;
2. allow `r <= 2M`;
3. remove `sin(theta)^2` from `g_phi_phi`;
4. flip the Riemann convention without transforming expected components;
5. change the passport's expected Kretschmann scalar;
6. supply a symbolic expression containing attribute access, import, file access, a float, or an excessive power.

Report exactly one outcome: `APPROVED`, `CHANGES_REQUIRED`, `REJECTED`, or `UNABLE_TO_VERIFY`. List every discrepancy and remaining objection. Explicitly state whether your review is independent of ChefMrFrizzle, OpenAI Codex, the repository's machine, and its credentials.

Return a machine-readable artifact plus a readable report. Sign the final artifact with your established GPG, SSH, or Sigstore identity, publish the detached signature and verification command, and distinguish the content digest from the signature. Do not claim that this established benchmark proves a novel geometry, engineering feasibility, traveler safety, or the Mars-distance thesis.

---
