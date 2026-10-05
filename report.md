# Day 01 — Automated DevSecOps Security Gate
## Full Project Report

---

## 1. Project Overview

| Field | Value |
|-------|-------|
| **Project Name** | Day 01 — Automated DevSecOps Security Gate |
| **Challenge** | 30 Days of Cybersecurity GitHub Portfolio |
| **Goal** | Demonstrate automated software security controls using GitHub Actions |
| **Host OS** | Bazzite Linux |
| **Local Path** | `/run/media/tanjidurrahman2414/Game Files/Cybersecurity/Projects/day-01-devsecops-security-gate/` |
| **Target Platform** | Public GitHub repository |
| **Compute Model** | GitHub-hosted runners (no local VMs, containers, CI servers, or databases required) |
| **Current Status** | Locally validated; GitHub Actions has not run yet |

---

## 2. What the Project Demonstrates

- **Automated DevSecOps pipeline** embedded in GitHub Actions
- **Secret scanning** with Gitleaks
- **Static Application Security Testing (SAST)** with GitHub CodeQL
- **Dependency and filesystem vulnerability scanning** with Trivy
- **Software Bill of Materials (SBOM)** generation with CycloneDX
- **Security gate behavior** suitable for pull requests
- **Least-privilege workflow permissions**
- **Secure GitHub Actions design** (no `pull_request_target`, actions pinned to full commit SHAs, no credentials in workflow files)
- **Professional documentation** for a public portfolio

---

## 3. Directory Structure

```text
day-01-devsecops-security-gate/
├── README.md
├── SECURITY.md
├── LICENSE
├── .gitignore
├── requirements.in
├── requirements.txt
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   └── test_app.py
│
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       ├── codeql.yml
│       ├── gitleaks.yml
│       └── trivy.yml
│
├── security/
│   ├── SECURITY-GATES.md
│   └── threat-model.md
│
├── sbom/
│   └── README.md
│
├── evidence/
│   ├── local-validation.md
│   ├── actions/
│   │   └── README.md
│   ├── codeql/
│   │   └── README.md
│   ├── gitleaks/
│   │   └── README.md
│   └── trivy/
│       └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── remediation.md
│   └── lessons-learned.md
│
└── diagrams/
    └── pipeline.mmd
```

---

## 4. File Inventory and Descriptions

### Root Documentation

| File | Purpose |
|------|---------|
| `README.md` | Professional portfolio overview, architecture, stack, workflows, local instructions, and project structure |
| `SECURITY.md` | Supported scope, no-real-secrets policy, safe testing expectations, and vulnerability reporting process |
| `LICENSE` | MIT License |
| `.gitignore` | Protects secrets, keys, local environments, generated scan outputs, and SBOM files |
| `requirements.in` | Direct runtime and test dependency constraints |
| `requirements.txt` | Pinned direct and transitive dependencies used for installation and scanning |
| `evidence/local-validation.md` | Results of pre-push tests and security scans |

### Application Code

| File | Purpose |
|------|---------|
| `app/__init__.py` | Package marker for the FastAPI application |
| `app/main.py` | Small FastAPI app with `GET /`, `GET /health`, `POST /notes`, and `GET /notes/{id}` endpoints |

### Tests

| File | Purpose |
|------|---------|
| `tests/test_app.py` | pytest suite covering all four API endpoints and input validation |

### GitHub Actions Workflows

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Runs pytest and generates/upload CycloneDX SBOM artifact |
| `.github/workflows/codeql.yml` | Runs GitHub CodeQL Python SAST analysis |
| `.github/workflows/gitleaks.yml` | Scans repository history for secrets |
| `.github/workflows/trivy.yml` | Scans filesystem and dependencies for MEDIUM or higher vulnerabilities |
| `.github/dependabot.yml` | Checks Python dependencies and GitHub Actions for updates weekly |

### Security Documentation

| File | Purpose |
|------|---------|
| `security/SECURITY-GATES.md` | Defines each security gate, fail conditions, and branch protection recommendations |
| `security/threat-model.md` | Identifies threats, impacts, mitigations, trust boundaries, and risk acceptance |

### Supporting Documentation

| File | Purpose |
|------|---------|
| `docs/architecture.md` | Full architecture description with Mermaid diagram |
| `docs/remediation.md` | Step-by-step remediation workflow for each failed gate |
| `docs/lessons-learned.md` | Placeholder for post-execution insights |
| `sbom/README.md` | Explains SBOM generation, artifact download, and non-commit policy |
| `evidence/*/README.md` | Placeholder instructions for scan result screenshots |

### Diagrams

| File | Purpose |
|------|---------|
| `diagrams/pipeline.mmd` | Mermaid source showing Developer → GitHub → GitHub Actions → Tests/Gitleaks/CodeQL/Trivy/SBOM → Security Gate → Approved/Blocked |

---

## 5. Application Architecture

The application is intentionally minimal so the security pipeline is the focus.

- **Framework:** FastAPI
- **Storage:** In-memory dictionary (no database)

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/notes` | Create a note (title + content) |
| GET | `/notes/{id}` | Retrieve a note by ID |

**Security features in the app:**

- Pydantic input validation with length limits
- HTTP 404 for missing resources
- No secrets, no eval/exec, no raw SQL
- A lock protects note IDs and the in-memory store during concurrent calls
- In-memory storage avoids a database but loses all notes on restart

---

## 6. Security Pipeline Detail

### Security Gates

| Gate | Workflow | Tool | Trigger | Fail Condition |
|------|----------|------|---------|----------------|
| Unit Tests | `ci.yml` | pytest | push `main`, PR | Any test fails |
| Secret Scan | `gitleaks.yml` | Gitleaks | push `main`, PR | Any detected secret |
| SAST | `codeql.yml` | CodeQL | push `main`, PR | Analysis failure; alert-based merge blocking requires a code-scanning ruleset |
| Dependency Scan | `trivy.yml` | Trivy | push `main`, PR | MEDIUM or higher CVE |
| SBOM Generation | `ci.yml` | CycloneDX | push `main`, PR | SBOM file missing |

### Pipeline Flow

```text
Developer pushes code or opens PR
            ↓
    GitHub Actions triggers
            ↓
    ┌───────┴───────┐
    ▼               ▼
 pytest        Gitleaks
    ▼               ▼
  CodeQL         Trivy
    ▼               ▼
 CycloneDX SBOM    │
    └───────┬───────┘
            ▼
    Security Gate
            ↓
    PASS → Approved / mergeable
    FAIL → Blocked / remediation required
```

---

## 7. Dependencies

### Runtime Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn[standard]` | ASGI server |
| `pydantic` | Data validation |

### Test Dependencies

| Package | Purpose |
|---------|---------|
| `pytest` | Test runner |
| `httpx2` | HTTP client used by FastAPI `TestClient` |

`requirements.in` declares the direct dependencies and `requirements.txt` locks the full tree. Both local development and CI install the lock, and Trivy scans it directly. Dependabot checks for Python and Action updates weekly.

### CI-Only Tools

| Tool | Purpose | Installation Location |
|------|---------|----------------------|
| `cyclonedx-bom` | SBOM generation | Installed during `ci.yml` run |
| `gitleaks/gitleaks-action` | Secret scanning | GitHub Action |
| `github/codeql-action` | SAST | GitHub Action |
| `aquasecurity/trivy-action` | Vulnerability scanning | GitHub Action |

---

## 8. Local Development Instructions

### Create a Virtual Environment

```bash
cd "/run/media/tanjidurrahman2414/Game Files/Cybersecurity/Projects/day-01-devsecops-security-gate"

python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8765
```

**Access points:**

- API root: `http://127.0.0.1:8765/`
- Health check: `http://127.0.0.1:8765/health`
- Swagger UI: `http://127.0.0.1:8765/docs`
- ReDoc: `http://127.0.0.1:8765/redoc`

### Run Unit Tests

```bash
pytest
```

### Example API Usage

```bash
curl -X POST http://127.0.0.1:8765/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Security Gate","content":"Automated checks are running."}'

curl http://127.0.0.1:8765/notes/1
```

---

## 9. GitHub Automation Summary

After the repository is pushed to GitHub, the following happens automatically:

### On Every Push to `main`

1. `ci.yml` runs pytest and generates an SBOM artifact
2. `codeql.yml` performs Python security analysis
3. `gitleaks.yml` scans the full commit history for secrets
4. `trivy.yml` scans the repository for MEDIUM or higher vulnerabilities

### On Every Pull Request to `main`

The same four workflows run against the PR branch. Results appear in:

- The pull request **Checks** tab
- The **Actions** tab
- The **Security → Code scanning alerts** tab (for CodeQL and Trivy)

### Artifacts Produced

| Artifact | Source | Content |
|----------|--------|---------|
| `sbom-cdx-json` | `ci.yml` | CycloneDX JSON SBOM of the Python environment |

---

## 10. Manual GitHub Configuration Required

The following must be configured in the GitHub web UI; they are not part of the committed files:

1. **Create a public GitHub repository** and push this project.
2. **Enable GitHub Actions** under Settings → Actions → General.
3. **Allow code scanning** for the public repository. The committed `codeql.yml` is an advanced setup; do not enable a second default CodeQL setup for the same code.
4. **Enable the dependency graph** (usually on by default for public repos).
5. **Configure branch protection for `main`:**
   - Check "Require a pull request before merging"
   - Check "Require status checks to pass before merging"
   - Add these status checks:
     - `CI / Run Tests and Generate SBOM`
     - `CodeQL / Analyze Python`
     - `Gitleaks / Secret Scan`
     - `Trivy / Filesystem and Dependency Scan`
   - Add a ruleset with **Require code scanning results**, select CodeQL, and set the alert threshold. Requiring the workflow job alone does not block on findings.
6. **Optionally enable Dependabot alerts** for continuous dependency monitoring.

---

## 11. Security Analysis

### Threats Addressed

| ID | Threat | Mitigation |
|----|--------|------------|
| T01 | Accidental secret commits | Gitleaks scans every push/PR |
| T02 | Vulnerable dependencies | Trivy scans for MEDIUM or higher CVEs |
| T03 | Common coding flaws | CodeQL SAST with security query suites |
| T04 | Regressions / broken security behavior | pytest validates functionality |
| T05 | Supply-chain opacity | CycloneDX SBOM generated per run |
| T06 | Malicious PR abuse of runner | No `pull_request_target`, least-privilege permissions |
| T07 | Compromised third-party actions | Full commit SHA pins and weekly Dependabot checks |

### Workflow Security Design

- **No `pull_request_target`:** prevents untrusted PR code from running with privileged credentials.
- **Least-privilege permissions:** each workflow declares only the permissions it needs.
- **Full commit SHA action pins:** moving tags cannot silently change the workflow action code; Dependabot proposes updates.
- **No credentials in workflow files:** `GITHUB_TOKEN` is provided by GitHub; an optional Gitleaks organization license is read from repository secrets.
- **No write permissions unless necessary:** only `security-events: write` is granted to CodeQL and Trivy for code-scanning results.

### Potential Security Concerns

| Concern | Detail | Mitigation |
|---------|--------|------------|
| Third-party action compromise | Actions from external orgs could be hijacked | Full commit SHA pins and review of Dependabot updates |
| Gitleaks licensing | Organization-owned repos require a license | Use a personal public repo or provide the organization license |
| Trivy false positives | MEDIUM or higher findings may not always be exploitable | Document and justify false positives; update dependencies |
| In-memory data loss | Notes disappear on application restart | Acceptable for demo; documented limitation |
| No authentication | API is open by design | Future enhancement; not needed for pipeline demo |
| Unbounded in-memory notes | Repeated writes can exhaust memory if the API is publicly exposed | Local demo only; add quotas and persistent storage before deployment |
| Workflow token scope | `security-events: write` is broader than read-only | Limited to code-scanning jobs |

---

## 12. Validation and Quality Checks Performed

| Check | Result |
|-------|--------|
| Python syntax validation (`python -m compileall`) | ✅ Pass |
| Workflow lint (`actionlint`) | ✅ Pass locally |
| Tests on Python 3.11, 3.12, and 3.14 | ✅ 7 passed on each version |
| Dependency integrity (`pip check`) | ✅ Pass locally |
| Dependency audit (`pip-audit`) | ✅ No known vulnerabilities at review time |
| Trivy filesystem scan | ✅ 29 pinned Python packages detected; no vulnerabilities at review time |
| Gitleaks directory scan | ✅ No leaks found locally |
| CycloneDX SBOM validation | ✅ Pass locally |
| Directory structure matches request | ✅ Pass |
| No obvious secrets in reviewed source files | ✅ Pass |
| `.gitignore` covers secrets, environments, generated artifacts | ✅ Pass |
| Workflows use least-privilege permissions | ✅ Pass |
| No `pull_request_target` used | ✅ Pass |
| No credentials in workflow files | ✅ Pass |
| Actions pinned to full commit SHAs | ✅ Pass |

The initial local audit found pytest 8.4.2 affected by PYSEC-2026-1845. The test constraint was raised to pytest 9.0.3 or later; the committed lock selects 9.1.1. The follow-up audit found no known vulnerabilities.

---

## 13. Risks and Limitations

- **CI has not executed yet:** workflows are validated locally but have not run on GitHub. GitHub results and screenshots are pending; local lessons are recorded.
- **Gitleaks action licensing:** organization-owned repositories require a Gitleaks license.
- **Dependency vulnerabilities:** the pinned lock passed a local advisory audit on 5 October 2026; new advisories can appear later.
- **In-memory storage:** not suitable for production use.
- **No deployment pipeline:** the project focuses on pre-merge security gates, not on secure deployment.
- **No input sanitization beyond Pydantic:** the simple note API does not require complex sanitization, but larger apps would need additional controls.

---

## 14. Manual Steps to Complete the Project

1. Push the project to a new public GitHub repository.
2. Enable GitHub Actions, CodeQL, and branch protection as described in Section 10.
3. Create a pull request with a small change to trigger the workflows.
4. Verify all four workflows pass.
5. Download the SBOM artifact from the CI workflow.
6. Capture screenshots of passing workflow runs and store them in `evidence/`.
7. Replace the GitHub-run **PENDING** sections in `README.md` and this report, and add GitHub-run lessons to `docs/lessons-learned.md`.
8. Add any findings and remediation notes to the documentation.

---

## 15. Conclusion

The Day 01 DevSecOps Security Gate project is prepared as a lightweight public portfolio repository. The local API, workflow syntax, dependency lock, scans, and SBOM have been checked. GitHub-hosted pipeline results remain unverified until the initial push and workflow run.

**Project status:** Ready to push to GitHub and execute CI. Scan results and evidence are pending the first workflow run.
