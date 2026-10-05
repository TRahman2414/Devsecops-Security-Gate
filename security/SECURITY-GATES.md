# Security Gates

This document defines the automated security gates that protect the `main` branch of this repository. Every push to `main` and every pull request must pass all gates before the code is considered safe to merge.

## Gate Overview

| Gate            | Workflow                          | Tool      | Fail Condition                                            |
|-----------------|-----------------------------------|-----------|-----------------------------------------------------------|
| Unit Tests      | `.github/workflows/ci.yml`        | pytest    | Any test fails.                                            |
| Secret Scan     | `.github/workflows/gitleaks.yml`  | Gitleaks  | Any detected secret or high-confidence credential pattern.|
| SAST            | `.github/workflows/codeql.yml`    | CodeQL    | Analysis failure; alerts block merging only after a code-scanning ruleset is configured. |
| Dependency Scan | `.github/workflows/trivy.yml`     | Trivy     | Any MEDIUM, HIGH, or CRITICAL vulnerability in dependencies. |
| SBOM Generation | `.github/workflows/ci.yml`        | CycloneDX | SBOM file is not generated or is invalid.                 |

## Gate Behavior

### Unit Test Gate

- Runs the test suite with `pytest`.
- Fails if any test returns a non-passing result.
- Serves as the baseline quality gate.

### Secret Scan Gate

- Scans the full repository history using Gitleaks.
- Fails if any pattern matching a known secret type is detected.
- Synthetic test values are not flagged if they do not match real patterns.

### SAST Gate

- Runs CodeQL with the `security-extended` and `security-and-quality` query suites.
- Results are uploaded to the GitHub Security tab.
- A finding does not necessarily fail the CodeQL workflow job. Configure a GitHub ruleset with **Require code scanning results**, select CodeQL, and choose the security-alert threshold to block merges on findings.

### Dependency Scan Gate

- Scans the committed, fully pinned `requirements.txt`, which includes direct and transitive dependencies.
- Reports vulnerabilities in Python dependencies found in the repository filesystem.
- Fails on MEDIUM, HIGH, or CRITICAL severity findings.
- SARIF upload is skipped for pull requests from forks, where the token cannot write code-scanning results; the vulnerability gate still runs.

### SBOM Gate

- Generates a CycloneDX JSON SBOM from the Python environment.
- Uploads `sbom.cdx.json` as a GitHub Actions artifact.
- Validates the SBOM and fails if generation or artifact upload fails.

## Handling Gate Failures

1. Open the failed workflow run in the GitHub Actions tab.
2. Read the failure summary and logs.
3. Determine which gate failed and why.
4. Apply the appropriate remediation from [`docs/remediation.md`](../docs/remediation.md).
5. Push the fix to the same branch.
6. Wait for all workflows to re-run and pass.

## Branch Protection Recommendation

After confirming the workflows run correctly, enable the following branch protection rules for `main`:

- Require a pull request before merging.
- Require status checks to pass before merging:
  - `CI / Run Tests and Generate SBOM`
  - `CodeQL / Analyze Python`
  - `Gitleaks / Secret Scan`
  - `Trivy / Filesystem and Dependency Scan`
- Add **Require code scanning results** with CodeQL and the desired alert threshold. Requiring the CodeQL workflow status alone only ensures that analysis ran successfully.

These settings are configured manually in the GitHub repository settings and are not part of the committed files.

## Exceptions

No automated exceptions are configured. If a finding is a false positive, it should be documented in the pull request and, if appropriate, suppressed using the tool's documented suppression mechanism (for example, a `.gitleaksignore` file or a Trivy ignore file).
