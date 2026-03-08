import streamlit as st
import csv
import random

# -------------------
# Load vocabulary
# -------------------
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
            vocab.append(
                {
                    "german": german,
                    "english": english,
                    "plural": plural,
                    "example": example,
                }
            )

if not vocab:
    st.error("Your vocab.csv file is empty or incorrectly formatted.")
    st.stop()


def setup_new_question() -> None:
    """Pick a new word and stable multiple-choice options."""
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


# -------------------
# Initialize session state
# -------------------
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0
if "answered_current_question" not in st.session_state:
    st.session_state.answered_current_question = False
if "round_complete" not in st.session_state:
    st.session_state.round_complete = False

if (
    "current_word" not in st.session_state
    or "options" not in st.session_state
    or "correct_answer" not in st.session_state
):
    setup_new_question()

word = st.session_state.current_word
correct_answer = st.session_state.correct_answer
options = st.session_state.options

# -------------------
# Viewport meta tag — prevents zoom/font-size issues on mobile
# -------------------
st.markdown(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
    unsafe_allow_html=True,
)

# -------------------
# Global styling (dark mode CSS)
# -------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Lock viewport scaling — backup for browsers that read this from CSS */
    @viewport {
        zoom: 1.0;
        width: device-width;
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
        --primary-color: var(--accent);
        --background-color: var(--app-bg);
        --secondary-background-color: var(--card-bg);
        --text-color: var(--text);
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
        top: 0;
        left: 0;
        right: 0;
        height: 52px;
        z-index: 999;
    }

    header[data-testid="stHeader"]::before,
    div[data-testid="stHeader"]::before {
        content: "HN";
        position: absolute;
        left: 16px;
        top: 10px;
        width: 30px;
        height: 30px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(79, 140, 255, 0.95), rgba(61, 220, 151, 0.75));
        color: #0b0d12;
        font-weight: 800;
        font-size: 0.78rem;
        letter-spacing: 0.02em;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.35);
        pointer-events: none;
    }

    header[data-testid="stHeader"]::after,
    div[data-testid="stHeader"]::after {
        content: "Haidar Neda";
        position: absolute;
        left: 54px;
        top: 13px;
        padding: 0.28rem 0.6rem;
        border-radius: 999px;
        background: rgba(26, 29, 36, 0.72);
        border: 1px solid rgba(79, 140, 255, 0.26);
        color: var(--text);
        font-weight: 600;
        font-size: 0.82rem;
        letter-spacing: 0.01em;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.28);
        pointer-events: none;
    }

    /* Hide Fork button and right-side header toolbar */
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

    div[data-testid="stAppViewContainer"] a {
        color: var(--accent);
        text-decoration: none;
    }
    div[data-testid="stAppViewContainer"] a:hover {
        text-decoration: underline;
    }

    .main {
        background-color: transparent;
    }

    /* Reduce Streamlit's default top padding */
    div[data-testid="stMainBlockContainer"] {
        padding-top: 2rem !important;
    }
    section[data-testid="stMain"] > div:first-child {
        padding-top: 2rem !important;
    }

    .app-wrapper {
        max-width: 700px;
        margin: 0 auto;
        padding: 0.5rem 1rem 3rem;
    }

    @media (min-width: 768px) {
        .app-wrapper {
            padding: 0.6rem 0 3.6rem;
        }
    }

    /* Compact header card */
    .app-header-card {
        background: #12141d;
        border-radius: 14px;
        padding: 0.65rem 1.4rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        border: 1px solid rgba(79, 140, 255, 0.32);
        margin-top: 0;
        margin-bottom: 0.85rem;
        position: relative;
        overflow: hidden;
    }

    .app-header-card::after {
        content: "";
        position: absolute;
        left: 0;
        bottom: 0;
        width: 38%;
        height: 2px;
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

    .meta-highlight {
        font-weight: 500;
        color: var(--accent);
    }

    .example-container {
        background: var(--card-bg-2);
        border-radius: 12px;
        padding: 0.65rem 0.8rem;
        margin-top: 0.35rem;
        border: 1px solid rgba(68, 78, 102, 0.75);
    }

    .stCheckbox > label, .stCheckbox span {
        font-size: 0.85rem;
        color: var(--text-muted);
    }

    .answer-area > div {
        margin-top: 0.45rem;
    }

    .answer-label {
        font-size: 0.9rem;
        color: #e1e4ec;
        margin-bottom: 0.45rem;
        font-weight: 500;
    }

    /* Radio cards — desktop */
    div.stRadio > div[role="radiogroup"],
    div[data-testid="stRadio"] > div,
    div[class*="stRadio"] > div {
        gap: 0.6rem;
    }

    div.stRadio > div[role="radiogroup"] > label,
    div[data-testid="stRadio"] > div > label,
    div[class*="stRadio"] > div > label {
        border-radius: 12px;
        padding: 0.65rem 0.9rem;
        border: 1px solid rgba(81, 92, 123, 0.9);
        background: #1f222b;
        display: flex;
        align-items: center;
        transition: all 0.18s ease-out;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.55);
        width: 100%;
        height: 58px;
        overflow: hidden;
    }

    div.stRadio > div[role="radiogroup"] > label:hover,
    div[data-testid="stRadio"] > div > label:hover,
    div[class*="stRadio"] > div > label:hover {
        border-color: #4f8cff;
        background: #252a35;
        box-shadow: 0 10px 22px rgba(79,
