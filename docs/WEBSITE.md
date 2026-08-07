# Public website architecture

## Purpose

The website is the public exploration layer for committed repository artifacts. It is not the scientific system of record and it does not run untrusted simulations.

## V0 decision

The public alpha is a dependency-free, statically generated multi-page site.

```text
web/pages.mjs + web/assets/*
              │
              ▼
scripts/build_site.mjs
              │
              ├── reads committed candidate/result/graph/agent/roadmap artifacts
              ├── renders eight HTML routes
              ├── copies raw evidence and project documents
              ├── generates project-status.json and llms.txt
              └── fingerprints every output in build-manifest.json
```

### Why static first

- The scientific artifacts are already immutable files.
- There is no need for authentication, a database, or server-side secrets in V0.
- A static build can be forked and hosted almost anywhere.
- The attack surface is smaller than a live job runner.
- Public claims can be reviewed directly in Git.
- Base-path support makes GitHub Pages and custom domains equivalent build targets.

## Routes

| Route | Purpose |
|---|---|
| `/` | Plain-language framing, current status, operating loop, and boundaries |
| `/lab/` | Candidate 000001, metric, checks, fingerprint, and limitations |
| `/graph/` | Interactive evidence graph and controlled-learning loop |
| `/agents/` | Agent roles, permissions, prohibitions, and handoffs |
| `/method/` | Hypothesis, objective terms, validation gates, and success ladder |
| `/learn/` | Beginner/technical concepts and reports from one result artifact |
| `/roadmap/` | Benchmark-gated phases and reusable protocol ideas |
| `/contribute/` | Reproduction, challenge, build, explanation, and setup paths |

## Artifact authority

The website may:

- change layout, navigation, and explanation level;
- calculate a clearly labeled browser convenience cross-check;
- visualize committed graph nodes and edges;
- construct repository contribution links.

The website may not:

- change result status;
- hide limitations or failed checks;
- present browser output as canonical science;
- call a remote model and display its output as evidence;
- execute community-submitted code;
- silently alter the published candidate or result.

## Build-time configuration

```text
PUBLIC_REPOSITORY_URL
PUBLIC_SITE_URL
PUBLIC_CONTACT_URL
PUBLIC_BASE_PATH
```

These variables are public metadata. Never put secrets in `PUBLIC_*` variables.

## Build and validation

```bash
npm ci
npm run build
npm run test:web
```

`npm run test:web` verifies required files, internal links, claim boundaries, artifact counts, full scientific digests, build fingerprints, JavaScript syntax, responsive accessibility primitives, and a GitHub Pages-style base-path build.

## V1 migration trigger

Do not add a server framework merely because the project is popular. Migrate from static hosting when a concrete requirement exists, such as:

- authenticated contributor workspaces;
- a reviewed candidate-submission queue;
- large queryable registries;
- signed reproduction uploads;
- isolated compute jobs;
- rate-limited APIs;
- moderation and abuse controls.

At that point, keep the current static site as a read-only export and preserve all canonical artifacts in portable formats.
