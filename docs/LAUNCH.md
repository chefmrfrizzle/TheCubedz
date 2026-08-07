# Launch runbook

## Definition of “launch today”

A professional V0 launch means:

- the full repository is public;
- the website is deployed from the repository;
- the baseline result is reproducible from a clean clone;
- limitations are visible on every important path;
- CI runs on each pull request;
- contributors have issue and pull-request templates;
- rollback is documented;
- no secret or private credential is committed.

It does **not** mean the research hypothesis has been proven.

## 1. Prepare the local repository

Use the provided repository with Git history. Do not place it inside another Git repository.

```bash
cd spacetime-research-release
npm ci
python -m pip install --no-build-isolation -e '.[dev]'
npm run check
```

Expected current baseline:

```text
Candidate: CANDIDATE-000001
Overall status: BASELINE_VERIFIED
Checks: 12 passed, 0 failed
Scientific payload digest:
sha256:91b67470ddfade1770e76793fef54d2f3812ad41f726bda16a3246fb2b428b4b
```

## 2. Create the GitHub repository

Create a new **empty public repository**.

Do not ask GitHub to generate another README, license, or `.gitignore` because those files already exist here.

The supplied history uses a neutral build identity. Before your first public push, configure the name and **verified email attached to your GitHub account**, then create one ownership commit. This makes future attribution and Git-triggered deployment authorization unambiguous.

```bash
git config user.name "<your GitHub display name>"
git config user.email "<your verified GitHub email or GitHub no-reply email>"
git commit --allow-empty -m "chore: initialize public repository ownership"

git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/chefmrfrizzle/TheCubedz.git
git branch -M main
git push -u origin main --follow-tags
```

Do not rewrite the supplied scientific commits merely to change their author. Your ownership commit becomes the public branch tip while preserving the reviewed release tag and history.

## 3. Set repository settings

Recommended settings:

- Require pull requests before merging once collaborators arrive.
- Require the `CI` checks after they have run successfully at least once.
- Require conversation resolution.
- Prevent force-pushes and branch deletion on `main`.
- Enable secret scanning and push protection where available.
- Enable Dependabot alerts and security updates.
- Enable Discussions for research questions and community orientation.
- Use Issues for bounded bugs, candidate proposals, challenges, and reproductions.

The current public repository settings were applied and recorded in [`GITHUB_SECURITY_SETTINGS.md`](GITHUB_SECURITY_SETTINGS.md). Re-verify them before release rather than assuming the record is current.

Do not enable CodeQL both through default setup and the committed advanced workflow at the same time. Choose one configuration.

## 4A. Deploy with Vercel

1. Open Vercel and select **Add New → Project**.
2. Import the GitHub repository.
3. Confirm:

```text
Build command: npm run build
Output directory: dist
```

`vercel.json` already supplies these settings and security headers.

4. Add:

```text
PUBLIC_REPOSITORY_URL=https://github.com/chefmrfrizzle/TheCubedz
PUBLIC_CONTACT_URL=https://github.com/chefmrfrizzle/TheCubedz/discussions
```

5. Deploy.
6. Copy the production URL and add:

```text
PUBLIC_SITE_URL=https://<production-domain>
```

7. Redeploy so canonical URLs, Open Graph metadata, `robots.txt`, and `sitemap.xml` use the final domain.

## 4B. Deploy with GitHub Pages

1. Open **Settings → Pages**.
2. Select **GitHub Actions** as the publishing source.
3. Open **Actions → Deploy public laboratory → Run workflow**.

The workflow computes the repository base path automatically, builds `dist/`, uploads the Pages artifact, and deploys it through the `github-pages` environment.

## 5. Post-deployment checks

Verify on desktop and mobile:

- overview page loads;
- all navigation routes load;
- Candidate 000001 renders 12 checks;
- the browser cross-check remains labeled noncanonical;
- the full digest is visible and copyable;
- graph search and filters work;
- beginner/technical explanation toggles work;
- raw JSON and Markdown files load;
- no browser console errors appear;
- repository and contact links point to the new repository;
- `/robots.txt`, `/llms.txt`, and `/build-manifest.json` load;
- the share card renders correctly when the URL is posted.

## 6. First public message

Use language like:

> I published an open computational research instrument for representing and challenging spacetime candidates. It currently verifies one intentionally ordinary flat-spacetime baseline. It has not found a wormhole or route to Mars. The goal is to make every proposal, failure, limitation, and reproduction inspectable. I am inviting physicists, scientific-computing engineers, skeptics, educators, and open-source contributors to test the instrument and help determine what should be built next.

Do not announce “AI solved spacetime,” “wormholes are possible,” or “we are getting to Mars.”

## 7. Rollback

### Vercel

Promote the last verified preview or use the Vercel rollback control. Do not rewrite Git history to hide a bad release.

### GitHub Pages

Revert the release commit on `main` and let the Pages workflow deploy the reverted artifact.

```bash
git revert <bad-commit-sha>
git push origin main
```

## 8. Release record

The supplied history archive is already tagged `v0.1.0-alpha.1`. Do **not** recreate or move that tag after the public push. Verify that it resolves to the checked release commit, and push it with the rest of the supplied annotated tags:

```bash
git describe --tags --exact-match HEAD
git push origin main --follow-tags
```

After deployment is verified, create a GitHub prerelease from the existing tag and include the exact scientific digest, checks, known limitations, and deployment URL.

For a later release, create a new version tag rather than reusing `v0.1.0-alpha.1`.
