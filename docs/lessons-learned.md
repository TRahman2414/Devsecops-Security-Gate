# Lessons Learned

> **Status:** Local and first GitHub-hosted results were recorded on 5 October 2026.

## What Worked

- The small FastAPI API was easy to verify with pytest and a live Swagger request.
- Separate workflows make test, secret, SAST, and dependency failures easy to identify.
- `actionlint`, Gitleaks, Trivy, and a dependency audit provided useful checks before publishing.

## Issues Found Locally

- The folder was initially not a Git repository, so none of its GitHub Actions workflows could run. It is now published as a public GitHub repository.
- Port 8000 was already occupied on the workstation. The documented example now uses port 8765.
- Loose dependency ranges caused each install to resolve independently and left Trivy without exact transitive versions. `requirements.in` now holds direct constraints; `requirements.txt` locks the full tree.
- The original pytest constraint selected a vulnerable 8.4.2 release. The lock now uses 9.1.1, and the local audit is clear.
- Action tags could move. Workflows now pin full commit SHAs, with Dependabot configured to propose updates.
- A successful CodeQL analysis job alone does not prove there are no findings. The repository ruleset checks CodeQL alert thresholds when merging.

## First GitHub Run

- The first CI run failed at test collection because invoking `pytest` directly did not include the repository root on Python's import path. Local `python -m pytest` had hidden the difference.
- Adding `pytest.ini` with `pythonpath = .` fixed both the documented local command and GitHub Actions. The next CI run passed all seven tests and generated the SBOM.
- Gitleaks, CodeQL, and Trivy also passed on `main`. Run links and the original CI failure are in [`evidence/actions/`](../evidence/actions/).
- Dependabot opened action-version updates immediately after publication. They should be reviewed as separate pull requests before merging.

## Next Validation

Verify a normal contributor pull request against the active repository ruleset. The first four successful runs were push events on `main`; Dependabot pull requests also triggered the workflows but are awaiting review.
