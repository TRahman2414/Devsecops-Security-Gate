# GitHub Actions Evidence

Validated on 5 October 2026 against commit `1595b8f` on `main`.

| Workflow | Result |
|---|---|
| [CI](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296218427) | Passed: seven tests, dependency check, CycloneDX SBOM generation and artifact upload |
| [Gitleaks](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296218423) | Passed |
| [CodeQL](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296218467) | Passed |
| [Trivy](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296218261) | Passed |

The CI run uploaded artifact `sbom-cdx-json` (artifact ID `11337919493`). It was downloaded and checked: CycloneDX 1.6 JSON, 29 components in the GitHub runner environment, including `httpx2`.

The first CI run failed because plain `pytest` could not import `app`. Commit `1595b8f` added `pytest.ini`; the next run passed. The failure is retained in [run 37296005486](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296005486) as remediation evidence.
