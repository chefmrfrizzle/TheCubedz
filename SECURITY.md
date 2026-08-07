# Security policy

## Supported versions

Security fixes target the current `main` branch and latest tagged prerelease. Older pre-alpha snapshots may not receive backports.

## Private reporting

Use GitHub's private vulnerability reporting feature under **Security → Advisories → Report a vulnerability** once enabled for the public repository.

When that feature is unavailable, contact the repository owner through their GitHub profile without posting exploit details publicly. Do not open a public issue containing credentials, an active account-compromise path, sandbox escape, or reproducible secret-exfiltration steps.

Include:

- affected commit/version;
- impact and attacker requirements;
- minimal reproduction;
- affected trust boundary;
- suggested mitigation, if known;
- whether the issue is already public.

## Scope

Report vulnerabilities involving:

- arbitrary code execution;
- dependency or workflow compromise;
- secret exposure;
- authentication or authorization;
- path traversal, injection, or unsafe file handling;
- scientific artifact tampering;
- provenance deletion or status injection;
- malicious candidate payloads;
- dataset poisoning or fabricated evidence pipelines;
- future compute-sandbox escape or resource abuse.

## Current architecture

The public V0 website is static and has no authentication, database, secret-bearing browser code, public job runner, or remote model call. The browser cross-check cannot write canonical state.

See [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md).

## Disclosure process

Maintainers should acknowledge a report, assess severity, coordinate a fix, and agree on disclosure timing. The project will credit reporters who request credit and act in good faith.

## Scientific integrity

Scientific integrity is also a security property. A polished interface, model output, or repeated agent statement must not be able to alter canonical scientific status without the declared evidence and review gates.
