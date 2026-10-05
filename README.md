# Day 01 — Automated DevSecOps Security Gate

> **Status:** Published on GitHub. The CI, Gitleaks, CodeQL, and Trivy workflows passed on `main` on 5 October 2026; the CycloneDX SBOM artifact was downloaded and checked.

---

## Project Overview

This project demonstrates a lightweight, automated DevSecOps security gate for a small Python web API. The goal is to show how modern security controls can be embedded directly into a GitHub-based development workflow without requiring local infrastructure, virtual machines, or heavy databases.

Every code change—whether a direct push to `main` or a pull request—triggers a pipeline that runs unit tests, secret scanning, static application security testing (SAST), dependency scanning, and software bill of materials (SBOM) generation. Each step acts as a security gate that must pass before the change can be trusted.

This repository is intentionally minimal. The application is small and the focus is on the security pipeline, reproducible configuration, and clear documentation.

---

## Problem Statement

Small development teams and security-minded individuals often struggle to:

- Detect secrets before they are merged into code.
- Identify vulnerable dependencies early.
- Catch common coding flaws through static analysis.
- Produce an auditable inventory of components.
- Enforce consistent security checks across every change.

This project solves those problems by wiring industry-standard, open-source security tools into a GitHub Actions pipeline that runs automatically on every contribution.

---

## Objectives

1. Build a small FastAPI application with basic endpoints.
2. Write unit tests using `pytest`.
3. Configure GitHub Actions to run the test suite on every push and pull request.
4. Integrate Gitleaks for secret scanning.
5. Integrate GitHub CodeQL for Python SAST.
6. Integrate Trivy for filesystem and dependency scanning.
7. Generate a CycloneDX JSON SBOM and store it as a workflow artifact.
8. Document security gates, threat model, and remediation workflow.
9. Produce evidence of successful pipeline execution.

---

## Architecture

```text
Developer
    |
    | git push / pull request
    v
GitHub Actions
    |
    +-- Unit Tests (pytest)
    |
    +-- Secret Scan (Gitleaks)
    |
    +-- SAST (CodeQL)
    |
    +-- Dependency/Repository Scan (Trivy)
    |
    +-- SBOM Generation (CycloneDX)
    |
    v
Security Gate
    |
    +-- PASS  --> Approved / mergeable
    |
    +-- FAIL  --> Remediation required
```

A Mermaid source version of this diagram is available in [`diagrams/pipeline.mmd`](diagrams/pipeline.mmd).

---

## Technology Stack

| Layer                | Technology                                              |
|----------------------|---------------------------------------------------------|
| Language / Framework | Python 3.11+, FastAPI                                   |
| Testing              | pytest, httpx2                                          |
| Secret Scanning      | Gitleaks                                                |
| SAST                 | GitHub CodeQL                                           |
| Dependency Scanning  | Aqua Security Trivy                                     |
| SBOM                 | CycloneDX Python BOM generator                          |
| CI/CD                | GitHub Actions (GitHub-hosted runners)                  |
| Version Control      | Git / GitHub                                            |

---

## Security Controls

| Control              | Tool        | Purpose                                                  |
|----------------------|-------------|----------------------------------------------------------|
| Unit Tests           | pytest      | Validate functional correctness and prevent regressions. |
| Secret Scanning      | Gitleaks    | Detect committed secrets, API keys, and tokens.          |
| Static Analysis      | CodeQL      | Find security vulnerabilities and coding flaws in Python.|
| Dependency Scanning  | Trivy       | Identify known vulnerabilities in dependencies.          |
| SBOM Generation      | CycloneDX   | Produce an inventory of components for supply-chain risk.|
| Least Privilege      | GitHub      | Workflows use minimal `permissions` blocks.              |

---

## Security Gates

A pull request or push to `main` must pass all of the following gates:

1. **Unit Test Gate:** All pytest tests pass.
2. **Secret Gate:** Gitleaks reports no detected secrets.
3. **SAST Gate:** CodeQL analysis runs; a GitHub code-scanning ruleset must be configured to block merges on findings.
4. **Dependency Gate:** Trivy reports no MEDIUM, HIGH, or CRITICAL vulnerabilities in the repository dependencies.
5. **SBOM Gate:** A valid CycloneDX SBOM is generated and attached as an artifact.

See [`security/SECURITY-GATES.md`](security/SECURITY-GATES.md) for detailed gate behavior and fail criteria.

---

## Workflows

| Workflow                        | File                              | Trigger                        | Purpose                                  |
|---------------------------------|-----------------------------------|--------------------------------|------------------------------------------|
| Continuous Integration          | `.github/workflows/ci.yml`        | push to `main`, pull_request   | Run tests, generate SBOM, upload artifact|
| Secret Scanning                 | `.github/workflows/gitleaks.yml`  | push to `main`, pull_request   | Scan repository history for secrets      |
| Static Application Security Test| `.github/workflows/codeql.yml`    | push to `main`, pull_request   | Run CodeQL Python analysis               |
| Dependency/Filesystem Scan      | `.github/workflows/trivy.yml`     | push to `main`, pull_request   | Scan dependencies and filesystem         |

---

## Local Development

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

`requirements.in` lists the direct dependencies. `requirements.txt` locks direct and transitive versions for repeatable local and CI installs. To refresh the lock after reviewing an update, install `uv` and run:

```bash
python -m pip install uv
uv pip compile requirements.in --universal --python-version 3.11 --upgrade --output-file requirements.txt
python -m pip install -r requirements.txt
python -m pip check
pytest
```

Dependabot checks Python packages and GitHub Actions weekly. Review its pull requests and rerun the lock command if the two requirement files drift.

### 3. Run the application

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8765
```

The API will be available at `http://127.0.0.1:8765`. This port avoids a local service already using 8000 on the development machine; choose another free port if needed.

The note store is in memory, unauthenticated, and cleared on restart. This API is a local security-pipeline demo, not a production note service.

Interactive API documentation is available at:

- Swagger UI: `http://127.0.0.1:8765/docs`
- ReDoc: `http://127.0.0.1:8765/redoc`

### 4. Run tests

```bash
pytest
```

### 5. GitHub Actions

The public repository is [TRahman2414/day-01-devsecops-security-gate](https://github.com/TRahman2414/day-01-devsecops-security-gate). The workflows run on pushes and pull requests targeting `main`. A repository ruleset requires pull requests, passing CI/Gitleaks/CodeQL/Trivy checks, and CodeQL results below its alert threshold before merging. This GitHub setting is separate from the committed workflow files.

---

## Threat Model Summary

The primary threats addressed by this pipeline are:

- **Secret leakage:** developers accidentally committing API keys, tokens, or passwords.
- **Known vulnerable dependencies:** outdated libraries with published CVEs.
- **Common coding flaws:** injection, unsafe deserialization, and other patterns detectable by SAST.
- **Supply-chain opacity:** inability to identify what components are included in the application.

See [`security/threat-model.md`](security/threat-model.md) for the full threat model.

---

## Evidence / Results

The first successful GitHub-hosted runs are recorded below. Each evidence page links to the original run.

| Evidence Type         | Location                                    | Status   |
|-----------------------|---------------------------------------------|----------|
| Actions summary       | [`evidence/actions/`](evidence/actions/)    | VERIFIED |
| CodeQL results        | [`evidence/codeql/`](evidence/codeql/)      | VERIFIED |
| Gitleaks results      | [`evidence/gitleaks/`](evidence/gitleaks/)  | VERIFIED |
| Trivy results         | [`evidence/trivy/`](evidence/trivy/)        | VERIFIED |
| Local pre-push checks | [`evidence/local-validation.md`](evidence/local-validation.md) | COMPLETE |

The initial CI run failed during test collection; a `pytest.ini` fix made plain `pytest` import the local package. The next run passed. Both runs are linked in the Actions evidence.

---

## Findings

The local pre-push review found that the original `pytest<9` constraint selected pytest 8.4.2, which has a published vulnerability ([PYSEC-2026-1845](https://github.com/pypa/advisory-database/blob/main/vulns/pytest/PYSEC-2026-1845.yaml)). The constraint now requires pytest 9.0.3 or later, and the lock selects 9.1.1. A fresh dependency audit found no known vulnerabilities.

The Trivy gate now fails on MEDIUM or higher findings. A temporary lock containing pytest 8.4.2 triggered the expected failure during local validation.

The original Trivy workflow scanned version ranges rather than the resolved dependency tree. It now scans the committed lock, including transitive packages. Local Trivy and Gitleaks scans passed; see [`evidence/local-validation.md`](evidence/local-validation.md). All four GitHub Actions workflows passed after the import fix.

---

## Remediation Workflow

When a security gate fails:

1. Review the failed workflow logs in the GitHub Actions tab.
2. Identify whether the failure is caused by a secret, vulnerable dependency, SAST finding, or test failure.
3. Apply the remediation guidance in [`docs/remediation.md`](docs/remediation.md).
4. Push the fix to the same branch.
5. Confirm all workflows pass before merging.

---

## Lessons Learned

Local pre-push lessons and the first GitHub-hosted CI failure are recorded.

A dedicated lessons-learned document is available at [`docs/lessons-learned.md`](docs/lessons-learned.md).

---

## Future Improvements

- Add OpenSSF Scorecard scanning.
- Add a dedicated deployment security gate if the API is ever deployed.
- Expand test coverage and add integration tests.
- Evaluate additional SAST tools for broader coverage.

---

## Project Structure

```text
day-01-devsecops-security-gate/
├── README.md
├── SECURITY.md
├── LICENSE
├── .gitignore
├── requirements.in
├── requirements.txt
├── pytest.ini
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_app.py
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       ├── codeql.yml
│       ├── gitleaks.yml
│       └── trivy.yml
├── security/
│   ├── SECURITY-GATES.md
│   └── threat-model.md
├── sbom/
│   └── README.md
├── evidence/
│   ├── local-validation.md
│   ├── actions/
│   ├── codeql/
│   ├── gitleaks/
│   └── trivy/
├── docs/
│   ├── architecture.md
│   ├── remediation.md
│   └── lessons-learned.md
└── diagrams/
    └── pipeline.mmd
```

---

## Disclaimer

This project is for authorized, defensive security education and portfolio development only. It does not contain real credentials, live attack tooling, or instructions for unauthorized access. All test values are synthetic.
