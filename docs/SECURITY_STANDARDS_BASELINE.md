# Security standards baseline

This file records the external security and governance references used to design the controlled-autonomy program. It is a project baseline, not a certification claim.

## AI risk and evaluation

- [NIST AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) - use lifecycle governance, pre-deployment testing, content provenance, incident handling, and explicit measurement rather than relying on model behavior alone.
- [NIST AI Risk Management Framework resources](https://airc.nist.gov/) - organize controls and evidence through the Govern, Map, Measure, and Manage functions.
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) - evaluate behavior hijacking, tool misuse, excessive privilege, identity abuse, memory poisoning, insecure inter-agent communication, cascading failure, and human-agent trust failures.

Project application: every model output remains untrusted working material; tools are separately authorized; deterministic evaluation and human promotion are mandatory.

## Secure software and CI/CD

- [NIST Secure Software Development Framework 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) - integrate secure practices throughout the software lifecycle and preserve evidence of those practices.
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use) - minimize token permissions, avoid privileged execution of untrusted pull-request content, protect secrets, and pin third-party actions to full commit SHAs.
- [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations) - generate and verify build provenance for released artifacts.
- [SLSA provenance specification 1.2](https://slsa.dev/spec/v1.2/provenance) - record verifiable information about where, when, and how an artifact was produced.

Project application: read-only pull-request workflows, protected release environments, immutable action references, dependency locks, provenance attestations, and a rebuildable release from a clean clone.

## Required review cadence

- Review this baseline before enabling authentication, model calls, public compute, new workflow write permissions, or a new artifact distribution path.
- Record the version or access date of a reference in the release review packet.
- Treat a change in a referenced standard as an input to threat review, not as an automatic repository change.
- Never describe adherence to this baseline as third-party validation, certification, or compliance unless such an assessment actually occurs.
