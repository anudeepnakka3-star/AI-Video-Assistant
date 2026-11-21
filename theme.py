"""Look and feel: warm butter paper, deep-green ink, serif display type, pill controls."""
import streamlit as st

STAGES = [
    "Reading the audio",
    "Transcribing the speech",
    "Naming the meeting",
    "Writing the summary",
    "Finding action items",
    "Finding decisions",
    "Collecting open questions",
    "Getting chat ready",
]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap');
:root{--butter:#FFFFEB;--ink:#0E2F28;--muted:#5C6B66;--line:#E6E4C9;
      --pink:#F9C5DB;--lilac:#DDD0FF;--mint:#CFEBD9;}
html,body,.stApp,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink);}
.stApp{background:var(--butter);}
header[data-testid="stHeader"]{background:transparent;}
#MainMenu,footer{visibility:hidden;}
.block-container{max-width:980px;padding-top:1.6rem;padding-bottom:6rem;}

/* type */
.brand{font-family:'Instrument Serif',serif;font-size:1.8rem;letter-spacing:-.01em;line-height:1;}
.hero{text-align:center;padding:3.2rem 0 2.2rem;}
.hero-title{font-family:'Instrument Serif',serif;font-size:clamp(2.8rem,7.2vw,5.4rem);
            line-height:1.02;letter-spacing:-.025em;margin:0 0 1.1rem;}
.hero-title em{font-style:italic;}
.hero p{max-width:33rem;margin:0 auto;color:var(--muted);font-size:1.1rem;line-height:1.55;}
.doc-title{font-family:'Instrument Serif',serif;font-size:clamp(2rem,4.6vw,3.1rem);
           line-height:1.08;letter-spacing:-.02em;margin:1.6rem 0 .4rem;}
.doc-meta{color:var(--muted);font-size:.95rem;margin-bottom:1.3rem;}

/* controls */
.stButton>button,.stDownloadButton>button{border-radius:999px;border:1px solid var(--line);
  background:#fff;color:var(--ink);font-weight:500;padding:.55rem 1.1rem;transition:border-color .15s;}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:var(--ink);color:var(--ink);background:#fff;}
button[kind="primary"],button[data-testid="stBaseButton-primary"]{
  background:var(--ink)!important;color:var(--butter)!important;border-color:var(--ink)!important;}
button[kind="primary"] p,button[data-testid="stBaseButton-primary"] p{color:var(--butter)!important;}
button:focus-visible{outline:2px solid var(--ink)!important;outline-offset:2px;}
.st-key-card-input .stButton>button{padding:.85rem 1.4rem;font-size:1.02rem;}
div[data-baseweb="input"],div[data-baseweb="select"]>div{border-radius:14px!important;background:#fff!important;
  border-color:var(--line)!important;}
section[data-testid="stFileUploaderDropzone"]{border-radius:18px;background:#fff;border:1.5px dashed #C9C7A6;}
.or{text-align:center;color:var(--muted);font-size:.9rem;margin:.2rem 0 .7rem;}

/* cards (st.container(key="card-...")) */
div[class*="st-key-card"]{background:#fff;border:1px solid var(--line);border-radius:26px;padding:1.7rem 1.9rem;}
div[class*="st-key-card"] .stMarkdown{line-height:1.65;}
div[class*="st-key-card"] li{margin-bottom:.35rem;}
[data-testid="stChatMessage"]{background:#fff;border:1px solid var(--line);border-radius:18px;}
[data-testid="stChatInput"]{border-radius:999px;}
.transcript{white-space:pre-wrap;line-height:1.7;max-height:520px;overflow-y:auto;}

/* category chips: pink = action, lilac = decision, mint = question (same everywhere) */
.chip{display:inline-block;padding:.28rem .8rem;border-radius:999px;font-size:.82rem;font-weight:600;
      border:1px solid var(--line);background:var(--butter);margin-bottom:.8rem;}
.chip.action{background:var(--pink);border-color:var(--pink);}
.chip.decision{background:var(--lilac);border-color:var(--lilac);}
.chip.question{background:var(--mint);border-color:var(--mint);}

/* landing demo: messy speech -> structured notes */
.demo{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:2.4rem;}
.demo-col{border-radius:26px;padding:1.6rem 1.7rem;}
.demo-col.raw{background:#F3F1D2;color:#46524D;line-height:1.7;}
.demo-col.clean{background:#fff;border:1px solid var(--line);}
.demo-label{font-weight:600;font-size:.9rem;margin-bottom:.8rem;color:var(--ink);}
.demo s{text-decoration-thickness:2px;text-decoration-color:#C2547F;opacity:.75;}
.demo-item{margin-bottom:.9rem;}
.demo-item p{margin:.1rem 0 0;line-height:1.5;}
@media(max-width:720px){.demo{grid-template-columns:1fr;}}

/* processing */
.progress{max-width:420px;margin:4rem auto;}
.progress ul{list-style:none;padding:0;margin:1.6rem 0 0;}
.progress li{padding:.5rem 0 .5rem 2rem;position:relative;color:var(--muted);font-size:1.02rem;}
.progress li::before{content:"";position:absolute;left:.3rem;top:.85rem;width:.8rem;height:.8rem;
  border-radius:50%;border:1.5px solid #C9C7A6;}
.progress li.done{color:var(--ink);}
.progress li.done::before{background:var(--ink);border-color:var(--ink);}
.progress li.now{color:var(--ink);font-weight:600;}
.progress li.now::before{background:#F27BA8;border-color:#F27BA8;animation:pulse 1.2s ease-in-out infinite;}
@keyframes pulse{50%{transform:scale(1.5);opacity:.5;}}
@media(prefers-reduced-motion:reduce){.progress li.now::before{animation:none;}}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def hero_html(app_name: str) -> str:
    return f"""
<div class="brand">{app_name}</div>
<div class="hero">
  <div class="hero-title">Don’t take notes,<br><em>just listen.</em></div>
  <p>Drop in a YouTube link or a recording. Get the summary, action items, decisions and open
  questions, then ask the meeting anything.</p>
</div>"""


def demo_html() -> str:
    return """
<div class="demo">
  <div class="demo-col raw">
    <div class="demo-label">What was said</div>
    So <s>um,</s> <s>Priya will,</s> actually no, Rahul will send the revised budget by <s>uh,</s> Thursday.
    We decided to push the launch to the 14th. <s>And,</s> still not sure who owns the vendor contract?
  </div>
  <div class="demo-col clean">
    <div class="demo-label">What you get</div>
    <div class="demo-item"><span class="chip action">Action item</span>
      <p>Rahul will send the revised budget by Thursday.</p></div>
    <div class="demo-item"><span class="chip decision">Decision</span>
      <p>The launch moves to the 14th.</p></div>
    <div class="demo-item"><span class="chip question">Open question</span>
      <p>Who owns the vendor contract?</p></div>
  </div>
</div>"""


def progress_html(current: int) -> str:
    items = []
    for i, label in enumerate(STAGES):
        cls = "done" if i < current else "now" if i == current else ""
        items.append(f'<li class="{cls}">{label}</li>')
    return ('<div class="progress"><div class="hero-title" style="font-size:2.6rem">Reading your meeting</div>'
            f'<ul>{"".join(items)}</ul></div>')
