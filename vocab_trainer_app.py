import streamlit as st
import csv
import random

vocab_file = "vocab.csv"
vocab = []
with open(vocab_file, encoding="utf-8-sig") as f:
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        if len(row) >= 2:
            german = row[0].strip()
            english = row[1].strip()
            plural = row[2].strip() if len(row) > 2 else ""
            example = row[3].strip() if len(row) > 3 else ""
            vocab.append({"german": german, "english": english, "plural": plural, "example": example})

if not vocab:
    st.error("Your vocab.csv file is empty or incorrectly formatted.")
    st.stop()


def setup_new_question() -> None:
    if "word_queue" not in st.session_state or not st.session_state.word_queue:
        shuffled = vocab.copy()
        random.shuffle(shuffled)
        st.session_state.word_queue = shuffled
        st.session_state.round_complete = True
    else:
        st.session_state.round_complete = False

    st.session_state.current_word = st.session_state.word_queue.pop()
    word = st.session_state.current_word
    correct = word["english"]
    wrong_answers = [w["english"] for w in vocab if w["english"] != correct]
    wrong_options = random.sample(wrong_answers, min(3, len(wrong_answers)))
    options = wrong_options + [correct]
    random.shuffle(options)
    st.session_state.correct_answer = correct
    st.session_state.options = options
    st.session_state.answered_current_question = False
    st.session_state.selected_answer = None
    st.session_state.answer_checked = False


if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0
if "answered_current_question" not in st.session_state:
    st.session_state.answered_current_question = False
if "round_complete" not in st.session_state:
    st.session_state.round_complete = False
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None
if "answer_checked" not in st.session_state:
    st.session_state.answer_checked = False

if ("current_word" not in st.session_state or "options" not in st.session_state or "correct_answer" not in st.session_state):
    setup_new_question()

word = st.session_state.current_word
correct_answer = st.session_state.correct_answer
options = st.session_state.options

# -------------------
# Fix viewport via JavaScript — overrides Streamlit's own meta tag
# -------------------
st.markdown(
    """
    <script>
        (function() {
            var existing = document.querySelector('meta[name="viewport"]');
            if (existing) { existing.parentNode.removeChild(existing); }
            var meta = document.createElement('meta');
            meta.name = 'viewport';
            meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0';
            document.head.appendChild(meta);
        })();
    </script>
    """,
    unsafe_allow_html=True,
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {
    -webkit-text-size-adjust: 100%;
    text-size-adjust: 100%;
    box-sizing: border-box;
}

:root {
    --app-bg: #0f1117;
    --app-bg-2: #05060a;
    --card-bg: #1a1d24;
    --card-bg-2: #222630;
    --accent: #4f8cff;
    --success: #3ddc97;
    --error: #ff6b6b;
    --text: #f5f7fa;
    --text-muted: #aab0bb;
}

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text);
}

div[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #181b24 0, var(--app-bg) 45%, var(--app-bg-2) 100%);
    color: var(--text);
}

header[data-testid="stHeader"],
div[data-testid="stHeader"] {
    background: rgba(15, 17, 23, 0.55);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(81, 92, 123, 0.35);
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 52px;
    z-index: 999;
}

header[data-testid="stHeader"]::before,
div[data-testid="stHeader"]::before {
    content: "HN";
    position: absolute;
    left: 16px; top: 10px;
    width: 30px; height: 30px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(79,140,255,0.95), rgba(61,220,151,0.75));
    color: #0b0d12;
    font-weight: 800;
    font-size: 0.78rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.35);
    pointer-events: none;
}

header[data-testid="stHeader"]::after,
div[data-testid="stHeader"]::after {
    content: "Haidar Neda";
    position: absolute;
    left: 54px; top: 13px;
    padding: 0.28rem 0.6rem;
    border-radius: 999px;
    background: rgba(26,29,36,0.72);
    border: 1px solid rgba(79,140,255,0.26);
    color: var(--text);
    font-weight: 600;
    font-size: 0.82rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.28);
    pointer-events: none;
}

header[data-testid="stHeader"] button[title*="Fork"],
header[data-testid="stHeader"] a[title*="Fork"],
header[data-testid="stHeader"] button[aria-label*="Fork"],
header[data-testid="stHeader"] [data-testid*="fork"],
header[data-testid="stHeader"] [class*="fork"],
div[data-testid="stHeader"] button[title*="Fork"],
div[data-testid="stHeader"] a[title*="Fork"],
div[data-testid="stHeader"] button[aria-label*="Fork"],
div[data-testid="stHeader"] [data-testid*="fork"],
div[data-testid="stHeader"] [class*="fork"],
header[data-testid="stHeader"] > div:last-child,
div[data-testid="stHeader"] > div:last-child {
    display: none !important;
}

div[data-testid="stAppViewContainer"] p,
div[data-testid="stAppViewContainer"] span,
div[data-testid="stAppViewContainer"] label,
div[data-testid="stAppViewContainer"] li,
div[data-testid="stAppViewContainer"] strong,
div[data-testid="stAppViewContainer"] em {
    color: var(--text);
}

div[data-testid="stAppViewContainer"] a { color: var(--accent); text-decoration: none; }
div[data-testid="stAppViewContainer"] a:hover { text-decoration: underline; }

.main { background-color: transparent; }

div[data-testid="stMainBlockContainer"] { padding-top: 2rem !important; }
section[data-testid="stMain"] > div:first-child { padding-top: 2rem !important; }

.app-wrapper {
    max-width: 700px;
    margin: 0 auto;
    padding: 0.5rem 1rem 3rem;
}

@media (min-width: 768px) {
    .app-wrapper { padding: 0.6rem 0 3.6rem; }
}

.app-header-card {
    background: #12141d;
    border-radius: 14px;
    padding: 0.65rem 1.4rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.45);
    border: 1px solid rgba(79,140,255,0.32);
    margin-top: 0;
    margin-bottom: 0.85rem;
    position: relative;
    overflow: hidden;
}

.app-header-card::after {
    content: "";
    position: absolute;
    left: 0; bottom: 0;
    width: 38%; height: 2px;
    background: linear-gradient(90deg, #4f8cff, transparent);
    opacity: 0.9;
}

.app-title {
    font-size: 1.55rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    color: #f5f7fa;
    margin: 0;
    line-height: 1.1;
}

.german-word {
    font-size: 1.75rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.4rem;
}

.meta-info {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 0.15rem;
    line-height: 1.4;
}

.meta-highlight { font-weight: 500; color: var(--accent); }

.stCheckbox > label, .stCheckbox span {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.answer-label {
    font-size: 0.9rem;
    color: #e1e4ec;
    margin-bottom: 0.45rem;
    font-weight: 500;
}

/* Option buttons — unselected */
.option-btn button {
    border-radius: 12px !important;
    padding: 0.55rem 0.5rem !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    border: 1px solid rgba(81,92,123,0.9) !important;
    background: #1f222b !important;
    color: #d5d8e4 !important;
    width: 100% !important;
    min-height: 58px !important;
    white-space: normal !important;
    line-height: 1.3 !important;
    transition: all 0.18s ease-out !important;
    box-shadow: 0 6px 14px rgba(0,0,0,0.55) !important;
    text-align: center !important;
}

.option-btn button:hover {
    border-color: #4f8cff !important;
    background: #252a35 !important;
    box-shadow: 0 10px 22px rgba(79,140,255,0.32) !important;
    transform: translateY(-1px) !important;
}

/* Selected option */
.option-btn-selected button {
    border-radius: 12px !important;
    padding: 0.55rem 0.5rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border: 2px solid #4f8cff !important;
    background: #262c3a !important;
    color: #ffffff !important;
    width: 100% !important;
    min-height: 58px !important;
    white-space: normal !important;
    line-height: 1.3 !important;
    box-shadow: 0 12px 26px rgba(79,140,255,0.4) !important;
    text-align: center !important;
}

/* Correct answer */
.option-btn-correct button {
    border-radius: 12px !important;
    padding: 0.55rem 0.5rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border: 2px solid #3ddc97 !important;
    background: #11241c !important;
    color: #3ddc97 !important;
    width: 100% !important;
    min-height: 58px !important;
    white-space: normal !important;
    line-height: 1.3 !important;
    box-shadow: 0 12px 26px rgba(61,220,151,0.35) !important;
    text-align: center !important;
}

/* Wrong answer */
.option-btn-wrong button {
    border-radius: 12px !important;
    padding: 0.55rem 0.5rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border: 2px solid #ff6b6b !important;
    background: #261119 !important;
    color: #ff6b6b !important;
    width: 100% !important;
    min-height: 58px !important;
    white-space: normal !important;
    line-height: 1.3 !important;
    box-shadow: 0 12px 26px rgba(255,107,107,0.3) !important;
    text-align: center !important;
}

.button-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
    margin-top: 0.95rem;
    margin-bottom: 0.25rem;
}

/* Check answer button */
div[data-testid="stButton"] > button[kind="primary"] {
    border-radius: 999px !important;
    padding: 0.55rem 1.4rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    background: linear-gradient(135deg, #4f8cff, #6fa8ff) !important;
    color: #ffffff !important;
    border: 1px solid rgba(118,162,255,0.9) !important;
    cursor: pointer !important;
    transition: all 0.16s ease-out !important;
