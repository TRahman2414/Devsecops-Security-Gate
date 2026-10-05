# Copy Ready Captions

## LinkedIn carousel post

I built a small FastAPI project to learn how a security gate behaves on a real pull request.

The first GitHub run failed during test collection because pytest couldn't import `app`. I added `pytest.ini`; the next run passed all seven tests. A dependency audit also found an affected pytest release, so I pinned a fixed version and reran the scans.

The repo now runs CI, Gitleaks, CodeQL and Trivy on pull requests. GitHub requires the checks before merge, and CI uploads a CycloneDX SBOM.

If you're learning DevSecOps, you can use it to follow a failed run through the fix: clone the repo, run the API and tests, then inspect the workflow files, run logs and SBOM. I left the failed run public so the troubleshooting path is visible.

Code, setup steps and evidence: https://github.com/TRahman2414/day-01-devsecops-security-gate

#DevSecOps #AppSec #GitHubActions

## LinkedIn image post

I built a small FastAPI notes API and put a security gate in front of `main`.

My first GitHub Actions run failed: `ModuleNotFoundError: No module named 'app'`. I added `pytest.ini`. The next run passed all seven tests. A dependency audit later caught pytest 8.4.2 (CVE-2025-71176), so I pinned 9.1.1 and reran the scans.

The images show the API, the pipeline, the dependency fix and the SBOM. If you want to try it, clone the repo and run the API and tests. Then compare the failed and passing runs in GitHub Actions. I kept both runs public because the fix is easier to understand when you can see what broke. CI, Gitleaks, CodeQL and Trivy are required before a PR can merge. CI also uploads a CycloneDX SBOM to inspect.

Setup, source code and run evidence: https://github.com/TRahman2414/day-01-devsecops-security-gate

#DevSecOps #AppSec #GitHubActions

## LinkedIn or Facebook video post

The first CI run for my DevSecOps demo failed. I found a pytest import problem and fixed it. The next run passed all four checks. This 42-second clip shows the app and the actual run history.

It's a local API demo, not a hosted notes app. The code and run logs are public: https://github.com/TRahman2414/day-01-devsecops-security-gate

## Facebook image post

I made this small Python project to learn what happens when security checks are required before code reaches main. The API is tiny. It has seven tests. My first CI run still broke on an import error.

I fixed it. The rerun passed, and I kept both runs in the repo. These nine images show what changed: https://github.com/TRahman2414/day-01-devsecops-security-gate
