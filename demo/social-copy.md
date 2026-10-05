# Copy Ready Captions

## LinkedIn carousel post

I built a small FastAPI project to learn how a security gate behaves on a real pull request.

The first GitHub run failed during test collection because pytest couldn't import `app`. I added `pytest.ini`; the next run passed all seven tests. A dependency audit also found an affected pytest release, so I pinned a fixed version and reran the scans.

The repo now runs CI, Gitleaks, CodeQL and Trivy on pull requests. GitHub requires the checks before merge, and CI uploads a CycloneDX SBOM.

If you're learning DevSecOps, you can use it to follow a failed run through the fix: clone the repo, run the API and tests, then inspect the workflow files, run logs and SBOM. I left the failed run public so the troubleshooting path is visible.

Code, setup steps and evidence: https://github.com/TRahman2414/day-01-devsecops-security-gate

#DevSecOps #AppSec #GitHubActions

## LinkedIn image post

I built a small FastAPI project to show what happens when security checks are required before a pull request can merge.

The images walk through the API, the first failed CI run, the fix and the passing security checks. I fixed the import path, and all seven tests passed on the next run. I also updated a vulnerable pytest version found during the dependency audit.

Want to try the same workflow? Clone the repo, run the API and tests locally, then open the Actions tab to compare the failed and passing runs. CI, Gitleaks, CodeQL and Trivy are required checks, and CI uploads a CycloneDX SBOM you can inspect.

Setup, source code and run evidence: https://github.com/TRahman2414/day-01-devsecops-security-gate

#DevSecOps #AppSec #GitHubActions

## LinkedIn or Facebook video post

The first CI run for my DevSecOps demo failed. I found a pytest import problem and fixed it. The next run passed all four checks. This 42-second clip shows the app and the actual run history.

It's a local API demo, not a hosted notes app. The code and run logs are public: https://github.com/TRahman2414/day-01-devsecops-security-gate

## Facebook image post

I made this small Python project to learn what happens when security checks are required before code reaches main. The API is tiny. It has seven tests. My first CI run still broke on an import error.

I fixed it. The rerun passed, and I kept both runs in the repo. These nine images show what changed: https://github.com/TRahman2414/day-01-devsecops-security-gate
