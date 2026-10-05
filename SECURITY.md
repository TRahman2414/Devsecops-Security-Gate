# Security Policy

## Supported Scope

This repository is a small, intentionally simple Python API used to demonstrate automated DevSecOps security controls in a GitHub Actions pipeline. Security reports should relate to:

- The application code in `app/`.
- The test code in `tests/`.
- The GitHub Actions workflow definitions in `.github/workflows/`.
- The dependency configuration in `requirements.in` and `requirements.txt`.

Out-of-scope items include:

- Third-party GitHub Actions themselves (report issues to their maintainers).
- Hypothetical vulnerabilities that require unrealistic deployment assumptions.
- Issues affecting local development environments outside the control of this project.

## No Real Secrets

This project does **not** contain real credentials, API keys, private keys, tokens, or certificates. Any values that resemble secrets are intentionally synthetic and used only for documentation or test purposes.

If a scan reports a finding inside this repository, please review the context carefully before treating it as a genuine leak.

## Safe Testing Expectations

If you choose to test this application locally or in a fork:

- Run it only on systems you own or control.
- Do not point scanners at infrastructure you do not own.
- Do not attempt to exploit live deployments without explicit authorization.
- Do not introduce malware, credential-harvesting code, or persistence mechanisms.

## Reporting a Vulnerability

If you discover a security issue within the supported scope:

1. Open a private GitHub Security Advisory for this repository if the repository settings allow it.
2. Alternatively, open a regular issue labeled `security` if the finding is not sensitive.
3. Provide enough detail to reproduce the issue, including affected files and steps.
4. Allow reasonable time for review before publicly disclosing.

## Response Process

- Reports will be acknowledged within a reasonable timeframe.
- Valid findings will be tracked through a GitHub issue or advisory.
- Fixes will be applied to the default branch when appropriate.
- This policy may be updated as the project evolves.
