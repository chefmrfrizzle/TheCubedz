# GitHub security settings record

Repository: `chefmrfrizzle/TheCubedz`

Verified on: 2026-08-07

## Main branch protection

- Pull request required before merge.
- One approving review required.
- Code-owner review required.
- Stale reviews dismissed after new commits.
- Approval required from someone other than the last pusher.
- `Public release contract` status check required and the branch must be current.
- Conversation resolution required.
- Linear history required.
- Administrators are included.
- Force pushes and branch deletion disabled.

## Repository security

- Secret scanning enabled.
- Push protection enabled.
- Dependabot vulnerability alerts enabled.
- Dependabot security updates enabled.
- Dependency update configuration covers npm, Python, and GitHub Actions.
- CodeQL uses the committed advanced workflow; do not enable a duplicate default setup.

## Deliberate limitations

- Signed commits are not required until maintainers have a documented signing and recovery procedure.
- Non-provider secret patterns and validity checks were not reported as enabled by the repository API.
- These settings protect the remote repository. They do not replace review of local commits, deployment configuration, Vercel access, or contributor identity.

Re-verify this record before each public release and after any ownership, organization, workflow, or authentication change.
