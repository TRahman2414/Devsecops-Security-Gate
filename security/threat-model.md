# Threat Model

## Scope

This threat model covers the small FastAPI application and its GitHub Actions CI/CD pipeline defined in this repository.

Out of scope:

- Production deployment infrastructure.
- Third-party GitHub Actions internal implementation details.
- GitHub platform-level security (handled by GitHub).

## Assumptions

- The repository is public on GitHub.
- Development occurs through pull requests or direct pushes to `main`.
- GitHub-hosted runners are used for CI/CD.
- No real credentials, keys, or tokens are committed to the repository.

## Identified Threats and Mitigations

| ID  | Threat                                                                 | Impact                                              | Mitigation                                                   |
|-----|------------------------------------------------------------------------|-----------------------------------------------------|--------------------------------------------------------------|
| T01 | A developer accidentally commits an API key or password.               | Secret exposure, unauthorized access.               | Gitleaks scans every push and pull request.                  |
| T02 | A dependency contains a known vulnerability (CVE).                     | Exploitation of the application or build pipeline.  | Trivy scans pinned dependencies and fails on MEDIUM or higher CVEs. |
| T03 | The application contains common coding flaws (e.g., injection).        | Remote code execution or data leakage.              | CodeQL runs SAST with security query suites.                 |
| T04 | A broken change is merged, causing regressions or insecure behavior.   | Unstable or insecure application.                   | pytest validates functional behavior.                        |
| T05 | The project lacks visibility into its components.                      | Slow incident response, supply-chain risk.          | CycloneDX SBOM is generated for every CI run.                |
| T06 | A malicious pull request exfiltrates secrets or abuses runner resources.| Credential theft, crypto-mining, data exfiltration. | Least-privilege permissions, no `pull_request_target`, no persisted checkout credentials, and job timeouts. |
| T07 | A third-party action is compromised or malicious.                      | Pipeline compromise.                                | Actions are pinned to full commit SHAs and reviewed through Dependabot updates.|
| T08 | The demo API is exposed to untrusted users.                            | Notes can be guessed by ID or memory exhausted by repeated writes. | Bind to localhost for demos; add authentication, quotas, and persistent storage before deployment. |

## Trust Boundaries

```text
Developer Workstation
        |
        | untrusted until merged
        v
   GitHub Repository  <-- secret scanning (Gitleaks)
        |
        v
  GitHub Actions Runner  <-- SAST (CodeQL), dependency scan (Trivy), tests, SBOM
        |
        v
   Merge to main  <-- only after all gates pass
```

## Risk Acceptance

- LOW and UNKNOWN dependency findings are reported but do not fail the Trivy job. SARIF is uploaded for same-repository runs; fork pull requests still run the vulnerability gate without SARIF upload.
- In-memory note storage means data is lost on restart. This is acceptable for a demonstration application.
- The note API is unauthenticated and has no write quota. It is intended for local demonstration only.
- Synthetic test values are accepted because they do not match real secret patterns.

## Future Enhancements

- Add OpenSSF Scorecard to evaluate repository security posture.
- Review Dependabot updates and enable dependency alerts on GitHub.
- Define a formal incident response process for genuine findings.
