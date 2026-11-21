"""Streamlit front end for the AI Video Assistant.  Run: streamlit run app.py"""
import html
import inspect
import re
import tempfile
import traceback
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="AI Video Assistant", page_icon="🎙️", layout="centered")

from core.rag_engine import ask_question  # noqa: E402
from main import run_pipeline  # noqa: E402
from theme import demo_html, hero_html, inject_css, progress_html  # noqa: E402
from utils.report import as_markdown, build_pdf, build_txt, needs_unicode_font  # noqa: E402

APP_NAME = "AI Video Assistant"
LANGUAGES = {"English (local Whisper)": "english", "Hindi or Hinglish (Sarvam AI)": "hinglish"}
MEDIA_TYPES = ["mp3", "wav", "m4a", "aac", "flac", "ogg", "mp4", "mov", "mkv", "webm"]
PANELS = {  # label -> (result key, chip style)
    "Summary": ("summary", ""),
    "Action items": ("action_items", "action"),
    "Decisions": ("key_decisions", "decision"),
    "Open questions": ("open_questions", "question"),
}
NAV = [*PANELS, "Transcript", "Chat"]
STARTERS = ["What were the main decisions?", "Who owns which action items?", "What is still unresolved?"]

S = st.session_state  # Streamlit reruns this script on every click, so everything lives here
for key, default in {"job": None, "result": None, "meta": {}, "panel": "Summary",
                     "messages": [], "exports": {}, "pending": None}.items():
    S.setdefault(key, default)
inject_css()


def brand():
    st.markdown(f'<div class="brand">{APP_NAME}</div>', unsafe_allow_html=True)


# ---------- 1. input ----------
def input_view():
    st.markdown(hero_html(APP_NAME), unsafe_allow_html=True)
    with st.container(key="card-input"):
        url = st.text_input("YouTube link", placeholder="https://www.youtube.com/watch?v=")
        st.markdown('<div class="or">or</div>', unsafe_allow_html=True)
        upload = st.file_uploader("Upload a recording", type=MEDIA_TYPES)
        lang = st.selectbox("Language spoken in the meeting", list(LANGUAGES))
        go = st.button("Create meeting notes", type="primary", use_container_width=True)
    if go:
        if upload is not None:  # the pipeline wants a path, so write the upload to disk
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(upload.name).suffix) as tmp:
                tmp.write(upload.getbuffer())
            S.job = {"source": tmp.name, "temp": True, "lang": lang, "label": upload.name}
            st.rerun()
        elif url.strip():
            S.job = {"source": url.strip(), "temp": False, "lang": lang, "label": url.strip()}
            st.rerun()
        else:
            st.warning("Paste a YouTube link or upload a recording to start.")
    st.markdown(demo_html(), unsafe_allow_html=True)


# ---------- 2. processing ----------
def processing_view():
    job = S.job
    brand()
    slot = st.empty()

    def on_progress(i):
        slot.markdown(progress_html(i), unsafe_allow_html=True)

    # Works with your original main.py. If run_pipeline has no `on_progress` argument,
    # show a single "working" message instead of the live stage list.
    live = "on_progress" in inspect.signature(run_pipeline).parameters
    if live:
        on_progress(0)
    else:
        slot.markdown('<div class="progress"><div class="hero-title" style="font-size:2.6rem">'
                      'Reading your meeting</div><p>Transcribing and analysing. Long videos can take '
                      'a few minutes.</p></div>', unsafe_allow_html=True)
    try:
        args = (job["source"], LANGUAGES[job["lang"]])
        result = run_pipeline(*args, on_progress=on_progress) if live else run_pipeline(*args)
    except Exception:
        S.job = None
        slot.empty()
        st.error("We couldn’t process this source. Check that the link is public, or that the file "
                 "plays on your computer, then try again.")
        with st.expander("Technical details"):
            st.code(traceback.format_exc())
        st.button("Back")
        return
    finally:
        if job["temp"]:
            Path(job["source"]).unlink(missing_ok=True)

    S.update(result=result, job=None, panel="Summary", messages=[], exports={},
             meta={"source": job["label"], "lang": job["lang"],
                   "words": len(str(result.get("transcript", "")).split())})
    st.rerun()


# ---------- 3. results ----------
def chat_panel(result):
    if not S.messages:
        st.caption("Ask anything about this meeting. Answers are drawn from the transcript.")
        for col, q in zip(st.columns(len(STARTERS)), STARTERS):
            if col.button(q, key=f"starter-{q}", use_container_width=True):
                S.pending = q
                st.rerun()
    for m in S.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    question = st.chat_input("Ask about this meeting") or S.pop("pending", None)
    if question:
        S.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Searching the transcript"):
                try:
                    answer = str(ask_question(result["rag_chain"], question))
                except Exception as e:
                    answer = f"I couldn’t answer that: {e}. Try rephrasing the question."
            st.markdown(answer)
        S.messages.append({"role": "assistant", "content": answer})


def results_view():
    r, meta = S.result, S.meta
    left, right = st.columns([4, 1])
    with left:
        brand()
    if right.button("New meeting", use_container_width=True):
        S.update(result=None, meta={}, messages=[], exports={}, panel="Summary")
        st.rerun()

    title = str(r.get("title", "Meeting notes")).strip().strip('"“”')
    st.markdown(f'<div class="doc-title">{html.escape(title)}</div>'
                f'<div class="doc-meta">{meta["words"]:,} words transcribed, {html.escape(meta["lang"])}</div>',
                unsafe_allow_html=True)

    if "pdf" not in S.exports:
        try:
            S.exports["pdf"] = build_pdf(r)
        except Exception:
            S.exports["pdf"] = None
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50] or "meeting-notes"
    c1, c2, _ = st.columns([1, 1, 2])
    c1.download_button("Download PDF", S.exports["pdf"] or b"", f"{slug}.pdf", "application/pdf",
                       disabled=S.exports["pdf"] is None, use_container_width=True)
    c2.download_button("Download TXT", build_txt(r).encode("utf-8"), f"{slug}.txt", "text/plain",
                       use_container_width=True)
    if needs_unicode_font(r):
        st.caption("This meeting contains non-Latin text. Add a Unicode font to assets/fonts to keep it "
                   "in the PDF. The TXT export is complete.")

    for col, label in zip(st.columns(len(NAV)), NAV):  # buttons, not st.tabs: tabs reset on every rerun
        if col.button(label, key=f"nav-{label}", use_container_width=True,
                      type="primary" if S.panel == label else "secondary"):
            S.panel = label
            st.rerun()
    st.write("")

    if S.panel == "Chat":
        chat_panel(r)
    elif S.panel == "Transcript":
        with st.container(key="card-transcript"):
            st.markdown(f'<div class="transcript">{html.escape(str(r.get("transcript", "")))}</div>',
                        unsafe_allow_html=True)
    else:
        key, chip = PANELS[S.panel]
        with st.container(key=f"card-{key}"):
            st.markdown(f'<span class="chip {chip}">{S.panel}</span>', unsafe_allow_html=True)
            st.markdown(as_markdown(r.get(key)) or "Nothing was found in this meeting.")


if S.job:
    processing_view()
elif S.result:
    results_view()
else:
    input_view()
