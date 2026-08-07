# Release checklist

## Scientific integrity

- [ ] Candidate and validator versions are explicit.
- [ ] `npm run verify:baseline` succeeds.
- [ ] `npm run verify:benchmark` executes all 100 frozen workflow cases without evaluator failure.
- [ ] `npm run verify:crosscheck` matches and remains labeled as not external reproduction.
- [ ] Result artifact has no unreviewed drift.
- [ ] Full scientific payload digest is recorded in release notes.
- [ ] Public language does not exceed the result scope.
- [ ] Limitations and transportation status remain visible.
- [ ] Reproduction count reflects actual independent records.

## Software quality

- [ ] `npm ci` succeeds from the lockfile.
- [ ] `python -m pip install --no-build-isolation -e '.[dev]'` succeeds.
- [ ] `npm run check` passes.
- [ ] Working tree is clean after verification.
- [ ] CI workflow YAML parses.
- [ ] No secret or local `.env` file is tracked.
- [ ] Dependency changes are reviewed.

## Website quality

- [ ] Desktop and mobile routes render.
- [ ] Internal links resolve.
- [ ] Keyboard navigation and visible focus work.
- [ ] Reduced motion is respected.
- [ ] Browser console has no errors.
- [ ] Candidate, result, graph, agent, and roadmap artifacts load.
- [ ] Evidence cube exposes all six faces with keyboard navigation and a semantic fallback.
- [ ] Repository/contact links point to production resources.
- [ ] Open Graph image and metadata render.
- [ ] `robots.txt`, `llms.txt`, and `build-manifest.json` load.

## Security

- [ ] Workflow permissions are least privilege.
- [ ] Every external GitHub Action is pinned to a reviewed full commit SHA.
- [ ] Release artifact provenance attestation is enabled.
- [ ] `main` branch protection and required checks match `GITHUB_SECURITY_SETTINGS.md`.
- [ ] Public variables contain no secrets.
- [ ] Content Security Policy is active on Vercel.
- [ ] No untrusted code runs in the website or deployment job.
- [ ] Security contact is valid.
- [ ] Rollback path is confirmed.

## Governance and communication

- [ ] Changelog is updated.
- [ ] Roadmap status is accurate.
- [ ] Known limitations are in the release notes.
- [ ] Public announcement uses claims-policy language.
- [ ] Git author email matches a verified GitHub account for the ownership commit.
- [ ] Tag is annotated and pushed.
- [ ] Release is marked prerelease while status is alpha.
