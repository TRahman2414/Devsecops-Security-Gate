# SBOM Directory

This directory is reserved for Software Bill of Materials (SBOM) artifacts.

## Generated SBOM

The CI workflow generates a CycloneDX JSON SBOM during every run:

- File: `sbom/sbom.cdx.json`
- Format: CycloneDX 1.6 JSON
- Tool: `cyclonedx-bom` Python package

The generator runs in a separate temporary environment so the SBOM describes the tested Python dependencies, not the SBOM tool itself.

## Do Not Commit Generated SBOMs

The generated `sbom.cdx.json` file is excluded from Git by `.gitignore` and is instead uploaded as a GitHub Actions artifact. This avoids repository bloat and ensures the SBOM always reflects the latest dependency tree.

## Downloading the SBOM

1. Open the latest successful `CI` workflow run on GitHub.
2. Navigate to the **Artifacts** section.
3. Download the `sbom-cdx-json` artifact.
4. Extract the `sbom.cdx.json` file.

## Evidence

After CI runs, a copy of the SBOM may be saved to [`evidence/actions/`](../evidence/actions/) for portfolio documentation.
