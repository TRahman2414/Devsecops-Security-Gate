# Lessons Learned

> **Status:** Local pre-push lessons are recorded. GitHub Actions results will be added after the first push.

## What Worked

- The small FastAPI API was easy to verify with pytest and a live Swagger request.
- Separate workflows make test, secret, SAST, and dependency failures easy to identify.
- `actionlint`, Gitleaks, Trivy, and a dependency audit provided useful checks before publishing.

## Issues Found Locally

- The folder was initially not a Git repository, so none of its GitHub Actions workflows could run. A local `main` repository is now initialized; a GitHub remote and push are still needed.
- Port 8000 was already occupied on the workstation. The documented example now uses port 8765.
- Loose dependency ranges caused each install to resolve independently and left Trivy without exact transitive versions. `requirements.in` now holds direct constraints; `requirements.txt` locks the full tree.
- The original pytest constraint selected a vulnerable 8.4.2 release. The lock now uses 9.1.1, and the local audit is clear.
- Action tags could move. Workflows now pin full commit SHAs, with Dependabot configured to propose updates.
- A successful CodeQL analysis job alone does not prove there are no findings. GitHub needs a code-scanning ruleset to block merges on alerts.

## Next Steps After Publishing

1. Verify all four GitHub Actions workflows on `main` and on a pull request.
2. Set branch protection and a CodeQL code-scanning ruleset using the actual check names.
3. Capture the first run's screenshots and SBOM artifact in the evidence folders.
4. Record any GitHub-hosted failures and their fixes here.
