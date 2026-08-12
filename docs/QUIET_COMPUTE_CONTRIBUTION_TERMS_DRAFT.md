# Quiet Compute contribution terms — draft

Status: **DRAFT — NOT YET ACCEPTING AUTOMATED PUBLIC SUBMISSIONS**

These terms are a technical and governance draft, not legal advice. They must be reviewed for the project's operating jurisdiction before a hosted intake service is enabled.

## What a participant controls

- Installation does not enroll a machine.
- Collection and validation run locally.
- There is no automatic telemetry or upload command.
- The participant selects each raw-artifact digest included in a submission bundle.
- Credentials, secrets, personal data, unrelated host data, and remote access are forbidden.
- A participant may stop using the local tools at any time.

## Ownership and permission

The participant retains ownership of data they have the right to contribute. Every measurement declares one publication scope and one commercial-use state before submission:

- `PUBLIC_AGGREGATE`, `PUBLIC_RAW_ARTIFACTS`, or `PRIVATE_REVIEW_ONLY`; and
- `ALLOWED`, `NOT_ALLOWED`, or `SEPARATE_AGREEMENT_REQUIRED` for commercial use.

The project may validate, reproduce, review, and publish only within the selected scope and applicable agreement. A public Git commit is durable and may be copied by others; a later withdrawal cannot reliably erase prior public history. Corrections and retractions remain visible.

## Compensation and commercial use

There is no payment, bounty, revenue share, employment, or equity promise in the current public program. Funding and donated compute cannot buy a scientific outcome and carry zero evidence-reputation weight.

The project may later offer paid software, validation, coordination, or research services. A future service may not silently expand the rights attached to an earlier contribution. Any compensated program needs separate written terms before the participant contributes under it.

## Scientific status

A submission is working evidence, not an accepted conclusion. Automated validation, replication count, contributor reputation, payment, or consensus cannot make it canonical. A named human review and the applicable evidence gates remain required.

## Privacy and security

Participants must use a non-production or otherwise authorized system and follow their organization's safety, privacy, export-control, employment, data, and equipment rules. Do not submit information that identifies workers or residents, exposes facility security, contains controlled technical data, or violates a third party's rights.

The project does not request remote access. Public job execution remains disabled. Security issues should follow [SECURITY.md](../SECURITY.md), not a public issue.

## Withdrawal, correction, and dispute

- Future collection can be stopped by the participant because enrollment is not automatic.
- Private-review material may be deleted subject to legal, security, and backup-retention requirements defined by the future hosted service.
- Public artifacts are corrected or retracted through append-only records rather than silently rewritten.
- Identity, independence, licensing, measurement, or attribution disputes pause promotion until a named human resolves them.

## Before hosted intake can open

The project must replace this draft with reviewed terms that identify the operating entity, governing law, privacy contact, retention periods, deletion process, data processors, incident process, permitted commercial uses, compensation rules if any, and versioned acceptance record.
