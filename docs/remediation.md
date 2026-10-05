# Remediation Workflow

This document describes how to respond when a security gate fails.

## General Steps

1. Open the failed workflow run in the GitHub Actions tab.
2. Identify which gate failed.
3. Read the failure logs carefully.
4. Apply the remediation guidance below for the specific gate.
5. Commit and push the fix to the same branch.
6. Confirm all workflows pass before merging.

## Unit Test Failures

**Symptom:** `CI / Run Tests and Generate SBOM` fails during the pytest step.

**Remediation:**

- Run tests locally: `pytest`
- Fix the failing assertion or application behavior.
- Ensure new code is covered by tests.
- Re-run CI.

## Secret Scan Failures

**Symptom:** `Gitleaks / Secret Scan` reports detected secrets.

**Remediation:**

1. Confirm whether the finding is a real secret or a false positive.
2. If real:
   - Revoke or rotate the exposed credential immediately.
   - Remove the secret from the repository history or rotate it if removal is not practical.
   - Store the secret in a secure vault or GitHub Secrets, never in source code.
3. If false positive (e.g., a synthetic test value):
   - Add the finding to `.gitleaksignore` following Gitleaks documentation.
   - Document why it is a false positive in the pull request.

## SAST Failures

**Symptom:** CodeQL reports a security alert or the code-scanning ruleset blocks a pull request.

**Remediation:**

1. Review the alert in the GitHub Security tab.
2. Determine if the finding is exploitable in the current context.
3. Refactor the code to remove the unsafe pattern.
4. Add or update tests to prevent regression.
5. If the alert is a false positive, dismiss it in the GitHub UI with a justification.

## Dependency Scan Failures

**Symptom:** `Trivy / Filesystem and Dependency Scan` reports MEDIUM, HIGH, or CRITICAL vulnerabilities.

**Remediation:**

1. Identify the vulnerable package from the Trivy output.
2. Check whether an updated version is available.
3. Update the direct constraint in `requirements.in` if needed, then regenerate `requirements.txt` with the `uv pip compile` command in the README. Commit both files.
4. Re-run the workflow.
5. If no patch is available, evaluate:
   - Whether the vulnerable code path is reachable.
   - Whether a temporary workaround is acceptable.
   - Document the risk in the pull request.

## SBOM Generation Failures

**Symptom:** `CI / Run Tests and Generate SBOM` fails to produce `sbom/sbom.cdx.json`.

**Remediation:**

- Check the `cyclonedx-py` command output for errors.
- Verify `requirements.txt` is syntactically valid.
- Ensure all listed packages can be installed.
- Re-run CI.

## Escalation

If a finding cannot be resolved quickly or its impact is unclear:

- Do not merge the pull request.
- Document the finding, affected component, and attempted fixes.
- Seek review from another maintainer or security contact.

## Prevention

- Run tests locally before pushing.
- Use pre-commit hooks for secret scanning where practical.
- Keep dependencies up to date.
- Follow secure coding practices reviewed in the threat model.
