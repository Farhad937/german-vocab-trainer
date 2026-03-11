import streamlit as st
import csv
import random

st.set_page_config(page_title="Deutsch Trainer", layout="wide")

vocab_file = "vocab.csv"
vocab = []
with open(vocab_file, encoding="utf-8-sig") as f:
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        if len(row) >= 2:
            vocab.append({
                "german":  row[0].strip(),
                "english": row[1].strip(),
                "plural":  row[2].strip() if len(row) > 2 else "",
                "example": row[3].strip() if len(row) > 3 else "",
            })

if not vocab:
    st.error("vocab.csv is empty or incorrectly formatted.")
    st.stop()


def setup_new_question():
    if "word_queue" not in st.session_state or not st.session_state.word_queue:
        q = vocab.copy(); random.shuffle(q)
        st.session_state.word_queue = q
        st.session_state.round_complete = True
    else:
        st.session_state.round_complete = False
    w = st.session_state.word_queue.pop()
    st.session_state.current_word = w
    correct = w["english"]
    wrongs = random.sample([v["english"] for v in vocab if v["english"] != correct], min(3, len(vocab)-1))
    opts = wrongs + [correct]; random.shuffle(opts)
    st.session_state.correct_answer  = correct
    st.session_state.options          = opts
    st.session_state.selected_answer  = None
    st.session_state.answer_checked   = False
    st.session_state.answered_current = False


for k, v in [("correct",0),("wrong",0),("answered_current",False),
             ("round_complete",False),("selected_answer",None),("answer_checked",False)]:
    if k not in st.session_state:
        st.session_state[k] = v

if "current_word" not in st.session_state:
    setup_new_question()

# ── Handle option-button click (stored in pending_pick, applied before render) ──
if "pending_pick" in st.session_state:
    st.session_state.selected_answer = st.session_state.pending_pick
    del st.session_state.pending_pick

word          = st.session_state.current_word
correct_answer = st.session_state.correct_answer
options       = st.session_state.options
selected      = st.session_state.selected_answer
checked       = st.session_state.answer_checked

# ── Styles ──────────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box;-webkit-text-size-adjust:100%}
:root{--bg:#0f1117;--bg2:#05060a;--accent:#4f8cff;--text:#f5f7fa;--muted:#aab0bb}
html,body,[class*="css"]{font-family:'Inter',system-ui,sans-serif;color:var(--text)}
div[data-testid="stAppViewContainer"]{background:radial-gradient(circle at top left,#181b24 0,var(--bg) 45%,var(--bg2) 100%)}
header[data-testid="stHeader"],div[data-testid="stHeader"]{background:rgba(15,17,23,.55);backdrop-filter:blur(10px);border-bottom:1px solid rgba(81,92,123,.35);position:fixed;top:0;left:0;right:0;height:52px;z-index:999}
header[data-testid="stHeader"]::before,div[data-testid="stHeader"]::before{content:"HN";position:absolute;left:12px;top:6px;width:40px;height:40px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(79,140,255,.95),rgba(61,220,151,.75));color:#0b0d12;font-weight:800;font-size:1rem;pointer-events:none}
header[data-testid="stHeader"]::after,div[data-testid="stHeader"]::after{content:"Haidar Neda";position:absolute;left:60px;top:10px;padding:.35rem .85rem;border-radius:999px;background:rgba(26,29,36,.72);border:1px solid rgba(79,140,255,.26);color:var(--text);font-weight:600;font-size:.92rem;pointer-events:none}
header[data-testid="stHeader"]>div:last-child,div[data-testid="stHeader"]>div:last-child,[data-testid*="fork"]{display:none!important}
.main{background-color:transparent}
div.block-container{max-width:100%!important;padding-top:1.2rem!important;padding-bottom:1.8rem!important;padding-left:2rem!important;padding-right:2rem!important}
div[data-testid="stMainBlockContainer"]{padding-top:.5rem!important}
.app-wrapper{max-width:1100px;margin:0 auto;padding:.5rem 1rem 2.5rem}
@media(min-width:768px){.app-wrapper{padding:.6rem 0 3.6rem}}
.app-header-card{background:#12141d;border-radius:14px;padding:.65rem 1.4rem;box-shadow:0 8px 24px rgba(0,0,0,.45);border:1px solid rgba(79,140,255,.32);margin-bottom:.85rem;position:relative;overflow:hidden}
.app-header-card::after{content:"";position:absolute;left:0;bottom:0;width:38%;height:2px;background:linear-gradient(90deg,#4f8cff,transparent)}
.app-title{font-size:2.4rem;font-weight:700;letter-spacing:.03em;color:#f5f7fa;margin:0;line-height:1.1}
.german-word{font-size:3.0rem;font-weight:700;color:#fff;margin-bottom:.75rem}
.meta-info{font-size:1.4rem;color:var(--muted);margin-bottom:.15rem;line-height:1.4}
.meta-highlight{font-weight:500;color:var(--accent)}
.answer-label{font-size:1.5rem;color:#e1e4ec;margin-bottom:.75rem;font-weight:600}

/* ── Option cards (pure HTML, no interactivity) ── */
.opt-grid{display:grid;grid-template-columns:1fr 1fr;gap:.65rem;margin-bottom:1.6rem}
.opt-card{border-radius:12px;padding:.6rem .9rem;font-size:1.2rem;font-weight:500;min-height:58px;display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.3;font-family:Inter,system-ui,sans-serif;box-shadow:0 6px 18px rgba(0,0,0,.55);cursor:pointer;transition:all .18s ease-out;border:1px solid rgba(42,110,110,.9);background:#1A3A3A;color:#cde8e8}
.opt-card:hover{background:#1f4545;border-color:#3d9e9e;transform:scale(1.02)}
.opt-card.selected{background:#1A3A3A;color:#fff;border:2px solid #5ecece;box-shadow:0 12px 28px rgba(94,206,206,.35)}
.opt-card.correct{background:#11241c;color:#3ddc97;border:2px solid #3ddc97;box-shadow:0 12px 26px rgba(61,220,151,.35);cursor:default}
.opt-card.wrong{background:#261119;color:#ff6b6b;border:2px solid #ff6b6b;box-shadow:0 12px 26px rgba(255,107,107,.3);cursor:default}
.opt-card.neutral{opacity:.6;cursor:default}

/* ── Invisible st.buttons that capture clicks ── */
.opt-btn-row{display:grid;grid-template-columns:1fr 1fr;gap:.65rem;margin-top:-1.6rem;margin-bottom:1.6rem}
.opt-btn-row div[data-testid="stButton"]>button{opacity:0!important;height:58px!important;min-height:58px!important;max-height:58px!important;border:none!important;background:transparent!important;box-shadow:none!important;padding:0!important;margin:0!important;cursor:pointer!important;width:100%!important;display:block!important}

/* ── Check / Next buttons ── */
div[data-testid="stButton"]>button[kind="primary"],
div[data-testid="stButton"]>button[kind="secondary"]{border-radius:999px!important;padding:.55rem 1.4rem!important;font-size:1.2rem!important;font-weight:500!important;background:linear-gradient(135deg,#4f8cff,#6fa8ff)!important;color:#fff!important;border:1px solid rgba(118,162,255,.9)!important;transition:all .16s ease-out!important;box-shadow:0 10px 24px rgba(0,0,0,.7)!important;width:100%!important}
div[data-testid="stButton"]>button[kind="primary"]:hover,
div[data-testid="stButton"]>button[kind="secondary"]:hover{filter:brightness(1.06)!important;transform:translateY(-1px)!important;box-shadow:0 16px 32px rgba(79,140,255,.55)!important}

.stAlert{border-radius:12px;padding:.7rem .9rem;border:1px solid transparent;box-shadow:0 10px 24px rgba(0,0,0,.65)}
.progress-card{background:#151822;border-radius:16px;padding:1.15rem 1.5rem 1.25rem;box-shadow:0 18px 40px rgba(0,0,0,.75);border:1px solid rgba(61,72,102,.7);margin-top:1.1rem}
.progress-header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.55rem}
.progress-title{font-size:1.4rem;font-weight:600;color:#f5f7fa}
.progress-subtitle{font-size:1.15rem;color:#8f95a3}
.stat-row{display:flex;flex-wrap:wrap;gap:.6rem 1rem;margin-top:.55rem}
.stat-pill{display:inline-flex;align-items:center;gap:.3rem;padding:.16rem .7rem;border-radius:999px;background:#202431;font-size:1.15rem;color:#d0d4e2;border:1px solid rgba(75,85,116,.9)}
.stat-pill--correct{background:#14291f;border-color:rgba(61,220,151,.7);color:#a9f0cd}
.stat-pill--wrong{background:#2a181c;border-color:rgba(255,107,107,.72);color:#ffc0c0}
.stat-pill--total{background:#202534;border-color:rgba(122,132,160,.9);color:#e0e4f3}
.stat-pill--remaining{background:#1c2030;border-color:rgba(79,140,255,.6);color:#b8caff}
.stProgress>div>div{background-color:#202636;border-radius:999px}
.stProgress>div>div>div{background:linear-gradient(90deg,#4f8cff,#3ddc97);border-radius:999px}
.tip-box{font-size:1.15rem;color:#8b92a0;margin-top:.95rem;line-height:1.5}

@media(max-width:640px){
    div[data-testid="stMainBlockContainer"]{padding-top:2rem!important}
    .app-title{font-size:2.8rem}
    .german-word{font-size:3.8rem}
    .meta-info{font-size:1.95rem}
    .answer-label{font-size:2rem}
    .opt-grid{gap:1.1rem;margin-bottom:2rem}
    .opt-btn-row{gap:1.1rem;margin-top:-2rem;margin-bottom:2rem}
    .opt-card{font-size:1.85rem;min-height:90px;padding:.85rem}
    .opt-btn-row div[data-testid="stButton"]>button{height:90px!important;min-height:90px!important;max-height:90px!important}
    .progress-title{font-size:1.8rem}
    .progress-subtitle{font-size:1.55rem}
    .stat-pill{font-size:1.55rem}
    .tip-box{font-size:1.55rem}
    div[data-testid="stButton"]>button[kind="primary"],
    div[data-testid="stButton"]>button[kind="secondary"]{font-size:1.75rem!important;padding:.8rem 1.4rem!important}
    header[data-testid="stHeader"]::before,div[data-testid="stHeader"]::before{left:10px;top:4px;width:40px;height:40px;font-size:1rem}
    header[data-testid="stHeader"]::after,div[data-testid="stHeader"]::after{left:58px;top:8px;font-size:.95rem;padding:.35rem .85rem}
}
</style>""", unsafe_allow_html=True)

# ── UI ──────────────────────────────────────────────────────────────────────────
st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="app-header-card"><div class="app-title">Deutsch Trainer</div></div>', unsafe_allow_html=True)

if st.session_state.get("round_complete"):
    st.success(f"🎉 You've reviewed all {len(vocab)} words! Starting a new round.")

st.markdown(f'<div class="german-word">{word["german"]}</div>', unsafe_allow_html=True)

col_left, _ = st.columns([2.2, 1.8])
with col_left:
    show_plural = st.checkbox("Show plural", value=True)
    if show_plural:
        if word["plural"]:
            st.markdown(f'<div class="meta-info"><span class="meta-highlight">Plural</span>: {word["plural"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="meta-info"><span class="meta-highlight">Plural</span>: not available</div>', unsafe_allow_html=True)
    show_example = st.checkbox("Show example", value=True)
    if show_example and word["example"]:
        st.markdown(f'<div class="meta-info">Example: {word["example"]}</div>', unsafe_allow_html=True)

st.markdown("<div class='answer-label'>Select the correct English meaning:</div>", unsafe_allow_html=True)

# ── Render styled HTML cards (display only) ──────────────────────────────────
def get_cls(option):
    if checked:
        if option == correct_answer: return "opt-card correct"
        if option == selected:       return "opt-card wrong"
        return "opt-card neutral"
    return "opt-card selected" if option == selected else "opt-card"

cards_html = '<div class="opt-grid">'
for opt in options:
    cards_html += f'<div class="{get_cls(opt)}">{opt}</div>'
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

# ── Render invisible st.buttons overlaid on top for click capture ─────────────
st.markdown('<div class="opt-btn-row">', unsafe_allow_html=True)
btn_col1, btn_col2 = st.columns(2)
btn_cols = [btn_col1, btn_col2, btn_col1, btn_col2]
for i, opt in enumerate(options):
    with btn_cols[i]:
        if st.button(opt, key=f"opt_{i}", use_container_width=True) and not checked:
            st.session_state.pending_pick = opt
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ── Check / Next ───────────────────────────────────────────────────────────────
check_col, next_col = st.columns(2)
with check_col:
    check_clicked = st.button("Check answer", key="check_btn", type="primary", use_container_width=True)
with next_col:
    next_clicked = st.button("Next word", key="next_btn", type="secondary", use_container_width=True)

if check_clicked:
    if st.session_state.selected_answer is None:
        st.warning("Please select an answer first.")
    elif not st.session_state.answer_checked:
        st.session_state.answer_checked = True
        if st.session_state.selected_answer == correct_answer:
            st.session_state.correct += 1
        else:
            st.session_state.wrong += 1
        st.session_state.answered_current = True
        st.rerun()

if next_clicked:
    setup_new_question()
    st.rerun()

if st.session_state.answer_checked:
    if st.session_state.selected_answer == correct_answer:
        st.success("✅ Correct! Well done, keep it up!")
    else:
        st.error(f"❌ Not quite. The correct answer is: **{correct_answer}**")

# ── Progress ───────────────────────────────────────────────────────────────────
total = st.session_state.correct + st.session_state.wrong
accuracy = (st.session_state.correct / total * 100) if total else 0.0
words_left = len(st.session_state.get("word_queue", []))

st.markdown('<div class="progress-card">', unsafe_allow_html=True)
st.markdown(f"""<div class="progress-header">
    <div class="progress-title">Session progress</div>
    <div class="progress-subtitle">{'Nice rhythm — keep going.' if total else 'Answer your first question to begin.'}</div>
</div>""", unsafe_allow_html=True)
st.progress(accuracy / 100)
st.markdown(f"""<div class="stat-row">
    <div class="stat-pill stat-pill--correct">✅ Correct: {st.session_state.correct}</div>
    <div class="stat-pill stat-pill--wrong">❌ Wrong: {st.session_state.wrong}</div>
    <div class="stat-pill stat-pill--total">📚 Total: {total}</div>
    <div class="stat-pill">🎯 Accuracy: {accuracy:.1f}%</div>
    <div class="stat-pill stat-pill--remaining">📖 Words left: {words_left} / {len(vocab)}</div>
</div>""", unsafe_allow_html=True)
st.markdown('<div class="tip-box">Edit <code>vocab.csv</code> anytime to add more words.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
