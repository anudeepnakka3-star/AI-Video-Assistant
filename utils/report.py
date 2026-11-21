"""Report helpers: normalise LLM output for display, build TXT and PDF exports."""
import re
from pathlib import Path

from fpdf import FPDF

# Optional: drop a Unicode TTF here to export non-Latin scripts (e.g. Devanagari) to PDF.
FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
FONT_REGULAR = FONT_DIR / "NotoSans-Regular.ttf"
FONT_BOLD = FONT_DIR / "NotoSans-Bold.ttf"

SECTIONS = [
    ("Summary", "summary"),
    ("Action items", "action_items"),
    ("Key decisions", "key_decisions"),
    ("Open questions", "open_questions"),
]


def _inline(x) -> str:
    if isinstance(x, dict):
        return "; ".join(f"{k}: {v}" for k, v in x.items())
    return str(x)


def as_markdown(value) -> str:
    """The extractors may return a string, list or dict; always give back markdown text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return "\n".join(f"- **{k}:** {_inline(v)}" for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return "\n".join(f"- {_inline(v)}" for v in value)
    return str(value)


def _plain(md: str) -> str:
    md = re.sub(r"\*\*|__|`", "", md)
    md = re.sub(r"^\s*#+\s*", "", md, flags=re.M)
    return re.sub(r"^\s*[-*]\s+", "• ", md, flags=re.M)


def build_txt(r: dict) -> str:
    title = str(r.get("title", "Meeting notes")).strip()
    parts = [title, "=" * len(title)]
    for label, key in SECTIONS:
        parts += ["", label.upper(), "-" * len(label), _plain(as_markdown(r.get(key))) or "Nothing found."]
    parts += ["", "TRANSCRIPT", "-" * 10, r.get("transcript", "")]
    return "\n".join(parts)


def _font_ready() -> bool:
    return FONT_REGULAR.exists() and FONT_BOLD.exists()


def needs_unicode_font(r: dict) -> bool:
    """True when the PDF would lose characters because no Unicode font is installed."""
    text = " ".join(str(r.get(k, "")) for k in ["transcript", "summary", "action_items",
                                                  "key_decisions", "open_questions", "title"])
    return (not _font_ready()) and any(ord(c) > 255 for c in text if c not in "“”‘’–—…•")


_ASCII = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-", "…": "...", "•": "-"})


def build_pdf(r: dict) -> bytes:
    pdf = FPDF(format="A4")
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(True, 18)
    pdf.add_page()

    if _font_ready():
        pdf.add_font("Body", "", str(FONT_REGULAR))
        pdf.add_font("Body", "B", str(FONT_BOLD))
        family, fit = "Body", (lambda s: s)
    else:
        family = "Helvetica"
        fit = lambda s: s.translate(_ASCII).encode("latin-1", "replace").decode("latin-1")

    def write(text, size=11, style="", after=3):
        pdf.set_font(family, style, size)
        pdf.multi_cell(0, size * 0.5, fit(text), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(after)

    write(str(r.get("title", "Meeting notes")).strip(), 20, "B", 6)
    for label, key in SECTIONS:
        write(label, 14, "B", 2)
        write(_plain(as_markdown(r.get(key))) or "Nothing found.")
        pdf.ln(3)
    write("Transcript", 14, "B", 2)
    write(r.get("transcript", ""), 10)
    return bytes(pdf.output())
