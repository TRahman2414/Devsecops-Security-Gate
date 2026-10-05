"""Build the shareable carousel, image slides, and silent captioned video.

Requires reportlab==5.0.1, Poppler's pdftoppm, and FFmpeg.
Run from anywhere with: python demo/build_demo.py
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
EXPORTS = ROOT / "exports"
SLIDES = EXPORTS / "slides"
PDF = EXPORTS / "devsecops-security-gate-carousel.pdf"
VIDEO = EXPORTS / "devsecops-security-gate-demo.mp4"
REPO_URL = "https://github.com/TRahman2414/day-01-devsecops-security-gate"

W, H = 1080, 1350
BG = HexColor("#0B1218")
SURFACE = HexColor("#13212A")
SURFACE_LIGHT = HexColor("#1A2B35")
RULE = HexColor("#31434C")
WHITE = HexColor("#F4F8F4")
MUTED = HexColor("#B1C0C0")
ACCENT = HexColor("#B9F36B")


def setup_fonts() -> None:
    candidates = {
        "Sans": "/usr/share/fonts/google-noto/NotoSans-Regular.ttf",
        "SansBold": "/usr/share/fonts/google-noto/NotoSans-Bold.ttf",
        "Mono": "/usr/share/fonts/dejavu-sans-fonts/DejaVuSansMono.ttf",
    }
    fallbacks = {"Sans": "Helvetica", "SansBold": "Helvetica-Bold", "Mono": "Courier"}
    for name, filename in candidates.items():
        if Path(filename).is_file():
            pdfmetrics.registerFont(TTFont(name, filename))
        else:
            globals()[f"FONT_{name.upper()}"] = fallbacks[name]
    globals().setdefault("FONT_SANS", "Sans")
    globals().setdefault("FONT_SANSBOLD", "SansBold")
    globals().setdefault("FONT_MONO", "Mono")


def rect(c: canvas.Canvas, x: float, y: float, w: float, h: float, color, radius=0) -> None:
    c.setFillColor(color)
    if radius:
        c.roundRect(x, y, w, h, radius, fill=1, stroke=0)
    else:
        c.rect(x, y, w, h, fill=1, stroke=0)


def label(c: canvas.Canvas, value: str, x: float, y: float, size=28, color=MUTED, font=None) -> None:
    c.setFillColor(color)
    c.setFont(font or FONT_SANS, size)
    c.drawString(x, y, value)


def lines(c: canvas.Canvas, values: list[str], x: float, y: float, size: float, leading: float, color=WHITE, font=None) -> None:
    for index, value in enumerate(values):
        label(c, value, x, y - index * leading, size, color, font or FONT_SANSBOLD)


def pill(c: canvas.Canvas, value: str, x: float, y: float, w: float, fill=ACCENT, text_color=BG) -> None:
    rect(c, x, y, w, 58, fill, 18)
    label(c, value, x + 20, y + 17, 24, text_color, FONT_SANSBOLD)


def base(c: canvas.Canvas, number: int, topic: str) -> None:
    rect(c, 0, 0, W, H, BG)
    c.setStrokeColor(HexColor("#1A2A32"))
    c.setLineWidth(1)
    for x in range(0, W + 1, 90):
        c.line(x, 0, x, H)
    for y in range(0, H + 1, 90):
        c.line(0, y, W, y)
    rect(c, 74, H - 88, 22, 22, ACCENT, 5)
    label(c, "DEVSECOPS TR  /  DAY 01", 112, H - 82, 24, WHITE, FONT_MONO)
    label(c, topic.upper(), 76, 137, 23, MUTED, FONT_MONO)
    c.setStrokeColor(RULE)
    c.line(76, 112, W - 76, 112)
    label(c, "@TRahman2414", 76, 57, 25, WHITE, FONT_SANSBOLD)
    label(c, f"{number:02d} / 09", W - 205, 57, 25, ACCENT, FONT_MONO)


def title(c: canvas.Canvas, values: list[str], y=1080, size=82, leading=96) -> None:
    lines(c, values, 76, y, size, leading, WHITE, FONT_SANSBOLD)


def draw_1(c: canvas.Canvas) -> None:
    base(c, 1, "Build log")
    rect(c, 76, 415, 12, 610, ACCENT, 6)
    lines(c, ["I built a", "security gate"], 118, 910, 104, 124)
    lines(c, ["A tiny FastAPI app.", "Four checks before merge."], 122, 645, 42, 60, MUTED, FONT_SANS)
    rect(c, 76, 225, 928, 146, SURFACE, 22)
    label(c, "LIVE ON GITHUB", 110, 307, 24, ACCENT, FONT_MONO)
    label(c, "4 / 4 checks passed on main", 110, 253, 39, WHITE, FONT_SANSBOLD)
    c.linkURL(REPO_URL, (76, 225, 1004, 371), relative=0)


def draw_2(c: canvas.Canvas) -> None:
    base(c, 2, "The first run")
    title(c, ["The first CI run", "failed."])
    label(c, "I found the issue in the test command.", 78, 850, 40, MUTED)
    rect(c, 76, 462, 928, 292, SURFACE, 22)
    rect(c, 76, 698, 928, 56, SURFACE_LIGHT, 22)
    label(c, "GITHUB ACTIONS / CI", 108, 713, 22, ACCENT, FONT_MONO)
    lines(c, ["ModuleNotFoundError:", "No module named 'app'"], 108, 618, 42, 64, WHITE, FONT_MONO)
    rect(c, 76, 264, 12, 126, ACCENT)
    lines(c, ["I added pytest.ini.", "The next run passed."], 118, 365, 42, 55, WHITE, FONT_SANSBOLD)


def endpoint(c: canvas.Canvas, y: float, method: str, path: str, detail: str) -> None:
    rect(c, 76, y, 928, 145, SURFACE, 18)
    pill(c, method, 102, y + 47, 122)
    label(c, path, 252, y + 79, 42, WHITE, FONT_MONO)
    label(c, detail, 252, y + 27, 27, MUTED)


def draw_3(c: canvas.Canvas) -> None:
    base(c, 3, "The app")
    title(c, ["A small API,", "tested end to end."])
    label(c, "7 passing tests  /  input validation  /  safe note IDs", 78, 848, 32, MUTED)
    endpoint(c, 640, "GET", "/health", "Health response: 200 OK")
    endpoint(c, 468, "POST", "/notes", "Create a note with validated fields")
    endpoint(c, 296, "GET", "/notes/{note_id}", "Read it back by ID")
    label(c, 'GET /health -> {"status":"healthy"}', 98, 226, 27, ACCENT, FONT_MONO)
    label(c, "POST /notes -> 201 Created, id=1", 98, 185, 27, ACCENT, FONT_MONO)


def gate(c: canvas.Canvas, x: float, y: float, name: str, detail: list[str], n: str) -> None:
    rect(c, x, y, 448, 250, SURFACE, 20)
    label(c, n, x + 27, y + 194, 29, ACCENT, FONT_MONO)
    label(c, name, x + 27, y + 131, 44, WHITE, FONT_SANSBOLD)
    lines(c, detail, x + 27, y + 74, 28, 38, MUTED, FONT_SANS)


def draw_4(c: canvas.Canvas) -> None:
    base(c, 4, "The pipeline")
    title(c, ["Every PR runs", "four checks."])
    label(c, "Each job has a clear pass or fail result.", 78, 854, 37, MUTED)
    gate(c, 76, 550, "CI + SBOM", ["Tests pass and a component", "inventory is uploaded."], "01")
    gate(c, 556, 550, "Gitleaks", ["Looks for committed", "secrets."], "02")
    gate(c, 76, 270, "CodeQL", ["Scans Python code for", "security findings."], "03")
    gate(c, 556, 270, "Trivy", ["Blocks medium or higher", "dependency findings."], "04")


def draw_5(c: canvas.Canvas) -> None:
    base(c, 5, "A real finding")
    title(c, ["The audit found a", "vulnerable pytest."])
    label(c, "The original range selected an affected release.", 78, 848, 35, MUTED)
    rect(c, 76, 445, 928, 316, SURFACE, 22)
    label(c, "BEFORE", 112, 694, 25, MUTED, FONT_MONO)
    label(c, "pytest 8.4.2", 112, 625, 51, WHITE, FONT_SANSBOLD)
    label(c, "CVE-2025-71176", 112, 570, 31, MUTED, FONT_MONO)
    c.setStrokeColor(RULE)
    c.setLineWidth(2)
    c.line(112, 535, 968, 535)
    label(c, "AFTER", 112, 490, 25, ACCENT, FONT_MONO)
    label(c, "pytest 9.1.1 pinned", 380, 486, 40, ACCENT, FONT_SANSBOLD)
    lines(c, ["I raised the minimum version,", "then reran pip-audit and Trivy."], 78, 350, 35, 52, WHITE, FONT_SANS)


def draw_6(c: canvas.Canvas) -> None:
    base(c, 6, "Supply chain")
    title(c, ["The build lists", "its components."])
    label(c, "CycloneDX 1.6 SBOM uploaded by CI.", 78, 851, 37, MUTED)
    rect(c, 76, 395, 928, 360, SURFACE, 22)
    label(c, "29", 111, 510, 170, ACCENT, FONT_SANSBOLD)
    lines(c, ["components in the", "GitHub runner artifact"], 440, 620, 40, 54, WHITE, FONT_SANSBOLD)
    label(c, "sbom-cdx-json", 112, 450, 35, WHITE, FONT_MONO)
    label(c, "Downloadable from the passing CI run", 78, 313, 32, MUTED)


def step(c: canvas.Canvas, y: float, n: str, text: str) -> None:
    rect(c, 76, y, 928, 105, SURFACE, 16)
    pill(c, n, 96, y + 23, 71)
    label(c, text, 194, y + 35, 38, WHITE, FONT_SANSBOLD)


def draw_7(c: canvas.Canvas) -> None:
    base(c, 7, "Enforcement")
    title(c, ["Passing runs", "protect main."])
    label(c, "The GitHub ruleset enforces the path to merge.", 78, 851, 34, MUTED)
    step(c, 682, "1", "Open a pull request")
    step(c, 548, "2", "Pass four required checks")
    step(c, 414, "3", "Clear CodeQL alert threshold")
    step(c, 280, "4", "Merge; force pushes blocked")


def metric(c: canvas.Canvas, x: float, y: float, value: str, detail: list[str]) -> None:
    rect(c, x, y, 448, 270, SURFACE, 20)
    label(c, value, x + 27, y + 129, 103, ACCENT, FONT_SANSBOLD)
    lines(c, detail, x + 27, y + 73, 28, 39, WHITE, FONT_SANS)


def draw_8(c: canvas.Canvas) -> None:
    base(c, 8, "At a glance")
    title(c, ["What shipped"], y=1087, size=96)
    label(c, "Verified on GitHub, 5 October 2026", 78, 945, 34, MUTED)
    metric(c, 76, 624, "4", ["required workflow", "checks"])
    metric(c, 556, 624, "7", ["passing API", "tests"])
    metric(c, 76, 324, "1", ["CycloneDX 1.6", "SBOM artifact"])
    metric(c, 556, 324, "0", ["open code scanning", "alerts at validation"])


def draw_9(c: canvas.Canvas) -> None:
    base(c, 9, "Open source")
    title(c, ["Explore the", "source and runs."], y=1064, size=89, leading=108)
    lines(c, ["The code, failed run, fix,", "passing checks, and SBOM", "are all public."], 78, 761, 40, 57, MUTED, FONT_SANS)
    rect(c, 76, 340, 928, 254, SURFACE, 22)
    label(c, "GITHUB", 111, 530, 25, ACCENT, FONT_MONO)
    lines(c, ["github.com/TRahman2414/", "day-01-devsecops-security-gate"], 111, 455, 31, 46, WHITE, FONT_MONO)
    c.linkURL(REPO_URL, (76, 340, 1004, 594), relative=0)
    label(c, "Built to be inspected, not just watched.", 78, 267, 33, WHITE)


DRAW = [draw_1, draw_2, draw_3, draw_4, draw_5, draw_6, draw_7, draw_8, draw_9]


def render_pdf() -> None:
    pdf = canvas.Canvas(str(PDF), pagesize=(W, H), pageCompression=1)
    pdf.setTitle("DevSecOps Security Gate - Social Demo Carousel")
    pdf.setAuthor("DevSecOps TR")
    for draw in DRAW:
        draw(pdf)
        pdf.showPage()
    pdf.save()


def render_pngs() -> list[Path]:
    renderer = shutil.which("pdftoppm")
    if renderer is None:
        raise RuntimeError("pdftoppm is required to render the carousel slides")
    result = []
    for page in range(1, len(DRAW) + 1):
        prefix = SLIDES / f"slide-{page:02d}"
        subprocess.run(
            [renderer, "-f", str(page), "-l", str(page), "-singlefile", "-png",
             "-scale-to-x", str(W), "-scale-to-y", str(H), str(PDF), str(prefix)],
            check=True,
        )
        result.append(prefix.with_suffix(".png"))
    return result


def render_video(pngs: list[Path]) -> None:
    encoder = shutil.which("ffmpeg")
    if encoder is None:
        raise RuntimeError("ffmpeg is required to build the demo video")
    command = [encoder, "-y", "-hide_banner", "-loglevel", "error"]
    for path in pngs:
        command += ["-loop", "1", "-t", "5", "-i", str(path)]
    filters = [f"[{i}:v]format=yuv420p,setsar=1,trim=duration=5,setpts=PTS-STARTPTS[v{i}]" for i in range(len(pngs))]
    previous = "v0"
    for i in range(1, len(pngs)):
        name = f"x{i}"
        filters.append(f"[{previous}][v{i}]xfade=transition=fade:duration=0.4:offset={i * 4.6:.1f}[{name}]")
        previous = name
    filters.append(f"[{previous}]fps=30,format=yuv420p[outv]")
    command += ["-filter_complex", ";".join(filters), "-map", "[outv]", "-an",
                "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-threads", "2",
                "-movflags", "+faststart", str(VIDEO)]
    subprocess.run(command, check=True)


def main() -> None:
    setup_fonts()
    SLIDES.mkdir(parents=True, exist_ok=True)
    render_pdf()
    render_video(render_pngs())
    print(PDF)
    print(VIDEO)


if __name__ == "__main__":
    main()
