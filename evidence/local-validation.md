# Local Pre-Push Validation

Date: 5 October 2026 (Singapore time)

These checks ran against the local project before its first GitHub push. The later GitHub-hosted results are linked in [`evidence/actions/`](actions/).

| Check | Result |
|---|---|
| `pytest` in clean Python 3.11, 3.12, and 3.14 environments | 7 passed on each version |
| `python -m pip check` with the pinned requirements | No broken requirements |
| `pip-audit -r requirements.txt` | No known vulnerabilities after updating pytest |
| Trivy 0.75.0 filesystem vulnerability scan and SARIF generation | Scanned `requirements.txt`; 0 vulnerabilities; valid SARIF 2.1.0 with 0 results |
| Trivy gate negative control | A temporary `pytest==8.4.2` requirements file produced MEDIUM finding CVE-2025-71176 and exit code 1 |
| Gitleaks 8.30.1 directory scan | No leaks found |
| `actionlint` workflow validation | No errors |
| CycloneDX 1.6 SBOM validation | Valid; 28 Linux/Python 3.12 components, including `httpx2`; generator excluded |

The initial audit found [PYSEC-2026-1845](https://github.com/pypa/advisory-database/blob/main/vulns/pytest/PYSEC-2026-1845.yaml) in pytest 8.4.2. `requirements.in` now requires pytest 9.0.3 or newer, and `requirements.txt` pins pytest 9.1.1.

GitHub-hosted CodeQL, Gitleaks, Trivy, tests, and SBOM artifact upload were confirmed after the first push; see [`evidence/actions/`](actions/).
