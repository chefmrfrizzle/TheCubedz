# External scientific review protocol

## Purpose

This protocol separates three questions that must not be collapsed:

1. Does the repository implementation behave as documented?
2. Does an outside specialist independently recover the scientific result?
3. Does any result support a novel geometry, physical mechanism, or transportation claim?

Candidate 000003 currently has internal support for question 1. Questions 2 and 3 remain open. A known-answer Schwarzschild match cannot prove the Mars thesis.

## Minimum qualified review record

A review intended to count as named scientific review must include:

- reviewer name and date;
- relevant field, qualification, and current affiliation or an equivalent public research record;
- a stable identity link such as an institutional page or ORCID when available;
- an explicit conflict-of-interest declaration, including prior collaboration, compensation, shared code, shared infrastructure, and AI assistance;
- the exact 40-character Git commit, candidate ID/version, passport ID/version, and result digest reviewed;
- the operating system, architecture, Python version, dependency versions, and exact commands;
- the tensor signature, Riemann convention, Ricci contraction, units, coordinate order, and domain interpreted by the reviewer;
- independent calculations or a separately identified solver, including every transformation needed to compare conventions;
- positive, negative, boundary, and adversarial cases actually checked;
- all discrepancies, exclusions, and unresolved objections;
- a bounded outcome: `APPROVED`, `CHANGES_REQUIRED`, `REJECTED`, or `UNABLE_TO_VERIFY`;
- a cryptographic signature over the final canonical record digest.

GitHub identity alone does not establish scientific qualification or independence. A content hash detects changes; it is not a signature and does not identify who approved the record.

## Reproduction levels

- R1: clean environment, same implementation.
- R2: independent implementation of the same method.
- R3: different validated solver or method.
- R4: independent physical experiment, only when a measurable prediction exists.

For Candidate 000003, the requested target is a named R3 reproduction on a separately controlled machine. The current project-owned SymPy and EinsteinPy paths do not qualify as outside reproduction.

## Signed artifact procedure

1. Save the final JSON or Markdown review record without a signature field.
2. Compute its SHA-256 digest using a documented canonicalization or sign the exact file bytes.
3. Sign with the reviewer's established GPG, SSH, or Sigstore identity.
4. Publish the record, detached signature, public-key identity, and verification command.
5. Verify the signature in CI and record the verification result without replacing the original artifact.

The project must not generate a key on the reviewer's behalf or call an unsigned internal artifact “signed.”

## Candidate 000003 scope

The review should confirm or challenge:

- the restricted symbolic parser cannot execute arbitrary submitted code;
- the passport scientific contract is exactly bound;
- the Schwarzschild exterior domain is `M > 0`, `r > 2M`, and `0 < theta < pi` in the declared chart;
- the complete nonzero Christoffel set and representative convention-sensitive Riemann components;
- vanishing Ricci and Einstein tensors in the exterior vacuum domain;
- Kretschmann scalar `48*M**2/r**6`;
- rejection of altered metrics, weakened domains, changed conventions, unsafe expressions, and modified passport expectations;
- honest exclusion of the interior, horizon-crossing coordinates, source reconstruction, geodesics, stability, traveler safety, engineering, and novel transportation conclusions.

## Promotion rule

One review may improve confidence in a benchmark but may not promote a Mars-related claim. Novel work requires its own preregistered candidate and falsification plan, source reconstruction, energy and conservation checks, causality and stability analysis, geodesic/travel objectives, traveler-safety bounds, at least one signed outside reproduction, and then qualified review of that specific claim.
