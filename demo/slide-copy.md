# Slide Copy and Voiceover

The nine slides follow the actual local API responses and GitHub run history. The metrics were verified on 5 October 2026.

1. **I built a security gate.** A tiny FastAPI app. Four checks before merge.
2. **The first CI run failed.** `pytest` could not import `app`; I added `pytest.ini` and the next run passed.
3. **A small API, tested end to end.** Health, note creation, note lookup, input validation, and unique IDs. Seven tests pass.
4. **Every PR runs four checks.** CI and SBOM, Gitleaks, CodeQL, and Trivy each report a result.
5. **The audit found a vulnerable pytest.** The original range selected 8.4.2. I raised the minimum and pinned 9.1.1.
6. **The build lists its components.** CI uploads a CycloneDX 1.6 SBOM. The verified GitHub artifact contained 29 components.
7. **Passing runs protect main.** A ruleset requires a pull request, four checks, and CodeQL results below its alert threshold.
8. **What shipped.** Four required checks, seven API tests, one SBOM artifact, and zero open code scanning alerts at validation time.
9. **Explore the source and runs.** The code, original CI failure, fix, passing runs, and SBOM are public at the repository link.

## Optional Voiceover (about 42 seconds)

I built a small FastAPI app to test a real security gate. The first GitHub run failed on a pytest import, so I fixed it. Every pull request now runs CI, Gitleaks, CodeQL, and Trivy. The dependency audit also found an affected pytest version, which I replaced and pinned. CI uploads a CycloneDX bill of materials. GitHub protects the main branch until the checks and CodeQL results pass. The code and run history are public.

The exported MP4 is silent, with the slide text baked in. Record this voiceover separately if you want narration.
