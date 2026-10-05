# Shareable Project Demo

These files tell the verified build story for the [DevSecOps Security Gate](https://github.com/TRahman2414/day-01-devsecops-security-gate). The API is a local demonstration, not a hosted production note service.

## Ready to post

| File | Use |
|---|---|
| [`exports/devsecops-security-gate-carousel.pdf`](exports/devsecops-security-gate-carousel.pdf) | Nine-page 4:5 document carousel for LinkedIn |
| [`exports/devsecops-security-gate-demo.mp4`](exports/devsecops-security-gate-demo.mp4) | 42-second silent, captioned 4:5 video for LinkedIn or Facebook |
| [`exports/slides/`](exports/slides/) | Nine ordered PNGs for an image post or album |
| [`social-copy.md`](social-copy.md) | LinkedIn and Facebook captions to copy and adapt |
| [`slide-copy.md`](slide-copy.md) | Slide text and optional voiceover |

The carousel is 43 KB, nine pages at 1080 x 1350. The H.264 video is 1080 x 1350, 30 fps, and about 1.4 MB. Keep the slide order `01` through `09` when posting the PNGs. The PDF and video contain no narration, copyrighted music, credentials, or real user data.

LinkedIn supports PDF document posts and MP4 video uploads. Its [document guide](https://www.linkedin.com/help/linkedin/answer/a518909) and [video guide](https://www.linkedin.com/help/linkedin/answer/a554265) describe current upload requirements. Facebook supports [photo and video posts](https://www.facebook.com/help/170116376402147); use the ordered PNGs as a photo post or upload the MP4 separately. Review the captions and evidence before posting.

## What the slides show

- The live local `/health` response returned `{"status":"healthy"}` and a sample `POST /notes` request created a note.
- The first CI run [failed on an import error](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296005486); commit `1595b8f` fixed it.
- [CI](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296218427), [Gitleaks](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296218423), [CodeQL](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296218467), and [Trivy](https://github.com/TRahman2414/day-01-devsecops-security-gate/actions/runs/37296218261) passed on `main`.
- CI uploaded a CycloneDX 1.6 SBOM; its downloaded GitHub artifact contained 29 components.
- GitHub's active `main` ruleset requires a pull request, four checks, and CodeQL results below its alert threshold. The code scanning API showed zero open alerts at validation time on 5 October 2026.

## Rebuild the assets

Install [ReportLab 5.0.1](https://pypi.org/project/reportlab/), Poppler (`pdftoppm`), and FFmpeg, then run:

```bash
python demo/build_demo.py
```

The builder rewrites the PDF, PNG slides, and MP4 in `demo/exports/`. It uses static, reviewed content; it does not contact GitHub or the local API during rendering. Refresh the numbers and links in the builder and copy files before reusing this demo for a later project state.
