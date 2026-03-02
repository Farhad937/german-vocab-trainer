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
    """Pick a new word and stable multiple‑choice options."""
    prev_word = st.session_state.get("current_word")
    prev_german = prev_word.get("german") if isinstance(prev_word, dict) else None

    st.session_state.current_word = random.choice(vocab)
    if prev_german and len(vocab) > 1:
        for _ in range(10):
            if st.session_state.current_word.get("german") != prev_german:
                break
            st.session_state.current_word = random.choice(vocab)

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
# Initialize session state (logic unchanged)
# -------------------
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0
if "answered_current_question" not in st.session_state:
    st.session_state.answered_current_question = False

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
# Global styling (dark mode CSS)
# -------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

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

        /* Streamlit theme variables (best-effort override) */
        --primary-color: var(--accent);
        --background-color: var(--app-bg);
        --secondary-background-color: var(--card-bg);
        --text-color: var(--text);
    }

    html, body, [class*="css"]  {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text);
    }

    div[data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, #181b24 0, var(--app-bg) 45%, var(--app-bg-2) 100%);
        color: var(--text);
    }

    div[data-testid="stHeader"] {
        background: transparent;
    }

    /* Ensure any default text stays readable on dark backgrounds */
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

    .app-wrapper {
        max-width: 700px;
        margin: 0 auto;
        padding: 1.8rem 1rem 3rem;
    }

    @media (min-width: 768px) {
        .app-wrapper {
            padding: 2.6rem 0 3.6rem;
        }
    }

    /* Header */
    .app-header-card {
        background: #12141d;
        border-radius: 18px;
        padding: 1.6rem 1.8rem 1.4rem;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.55);
        border: 1px solid rgba(79, 140, 255, 0.32);
        margin-bottom: 1.9rem;
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
        font-size: 1.9rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        color: #f5f7fa;
        margin-bottom: 0.3rem;
    }

    .app-tagline {
        font-size: 0.95rem;
        font-weight: 400;
        color: #aab0bb;
    }

    /* Question card */
    .question-card {
        background: #1a1d24;
        border-radius: 16px;
        padding: 1.6rem 1.5rem 1.25rem;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.7);
        margin-bottom: 1.3rem;
        border: 1px solid rgba(68, 78, 102, 0.6);
    }

    .question-header-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #6c7485;
        margin-bottom: 0.35rem;
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

    .example-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #81889a;
        letter-spacing: 0.12em;
        margin-bottom: 0.18rem;
    }

    .example-text {
        font-size: 0.9rem;
        color: #d3d7e2;
        line-height: 1.5;
    }

    .controls-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem 1rem;
        margin-top: 0.3rem;
        margin-bottom: 0.3rem;
    }

    .stCheckbox > label, .stCheckbox span {
        font-size: 0.85rem;
        color: var(--text-muted);
    }

    /* Answer area */
    .answer-area > div {
        margin-top: 0.45rem;
    }

    .answer-label {
        font-size: 0.9rem;
        color: #e1e4ec;
        margin-bottom: 0.45rem;
        font-weight: 500;
    }

    /* Radio as cards */
    div.stRadio > div[role="radiogroup"] {
        gap: 0.6rem;
    }

    div.stRadio > div[role="radiogroup"] > label {
        border-radius: 12px;
        padding: 0.65rem 0.9rem;
        border: 1px solid rgba(81, 92, 123, 0.9);
        background: #1f222b;
        display: flex;
        align-items: center;
        transition: all 0.18s ease-out;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.55);
    }

    div.stRadio > div[role="radiogroup"] > label:hover {
        border-color: #4f8cff;
        background: #252a35;
        box-shadow: 0 10px 22px rgba(79, 140, 255, 0.32);
        transform: translateY(-1px);
    }

    div.stRadio > div[role="radiogroup"] > label div[role="radio"] {
        margin-right: 0.6rem;
    }

    div.stRadio > div[role="radiogroup"] > label span {
        color: #d5d8e4 !important;
        font-size: 0.9rem;
    }

    /* Some Streamlit versions render radio text inside <p> */
    div.stRadio > div[role="radiogroup"] > label p {
        color: #d5d8e4 !important;
        margin: 0 !important;
    }

    /* Selected state */
    div.stRadio > div[role="radiogroup"] > label[data-checked="true"],
    div.stRadio > div[role="radiogroup"] > label:has(input:checked) {
        border-color: var(--accent);
        background: #262c3a;
        box-shadow: 0 12px 26px rgba(79, 140, 255, 0.4);
    }

    /* Buttons row */
    .button-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        margin-top: 0.95rem;
        margin-bottom: 0.25rem;
    }

    .stButton > button {
        border-radius: 999px !important;
        padding: 0.55rem 1.4rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        border: 1px solid rgba(81, 92, 123, 0.9) !important;
        cursor: pointer !important;
        transition: all 0.16s ease-out !important;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.7) !important;
        background: var(--card-bg-2) !important;
        color: var(--text) !important;
    }

    /* Primary: Check answer */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent), #6fa8ff) !important;
        color: #ffffff !important;
        border: 1px solid rgba(118, 162, 255, 0.9) !important;
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        filter: brightness(1.06);
        transform: translateY(-1px);
        box-shadow: 0 16px 32px rgba(79, 140, 255, 0.55) !important;
    }

    /* Secondary: Next word */
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: var(--card-bg-2) !important;
        color: var(--text) !important;
        border: 1px solid rgba(79, 140, 255, 0.7) !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background: #262b36 !important;
        transform: translateY(-1px);
        box-shadow: 0 14px 30px rgba(79, 140, 255, 0.28) !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"]:disabled,
    div[data-testid="stButton"] > button[kind="secondary"][disabled] {
        opacity: 0.45 !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
        transform: none !important;
        border-color: rgba(81, 92, 123, 0.9) !important;
        background: #20232b !important;
        color: #777e90 !important;
    }

    /* Extra hover glow for both buttons */
    div[data-testid="stButton"] > button:hover {
        filter: brightness(1.03);
    }

    /* Feedback messages – override default Streamlit alerts */
    .stAlert {
        border-radius: 12px;
        padding: 0.7rem 0.9rem;
        border: 1px solid transparent;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.65);
        background: transparent;
    }

    .stAlert > div {
        padding: 0 !important;
    }

    .stAlert-success {
        background-color: #11241c !important;
        border-color: rgba(61, 220, 151, 0.6) !important;
        color: #c9f6e3 !important;
    }

    .stAlert-error {
        background-color: #261119 !important;
        border-color: rgba(255, 107, 107, 0.7) !important;
        color: #ffd4d4 !important;
    }

    .stAlert-success * { color: #c9f6e3 !important; }
    .stAlert-error * { color: #ffd4d4 !important; }

    /* Progress section */
    .progress-card {
        background: #151822;
        border-radius: 16px;
        padding: 1.15rem 1.5rem 1.25rem;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.75);
        border: 1px solid rgba(61, 72, 102, 0.7);
        margin-top: 1.1rem;
    }

    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.55rem;
    }

    .progress-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #f5f7fa;
    }

    .progress-subtitle {
        font-size: 0.8rem;
        color: #8f95a3;
    }

    .stat-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem 1rem;
        margin-top: 0.55rem;
        font-size: 0.86rem;
        color: #d0d4e2;
    }

    .stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.16rem 0.7rem;
        border-radius: 999px;
        background: #202431;
        font-size: 0.8rem;
        color: #d0d4e2;
        border: 1px solid rgba(75, 85, 116, 0.9);
    }

    .stat-pill--correct {
        background: #14291f;
        border-color: rgba(61, 220, 151, 0.7);
        color: #a9f0cd;
    }

    .stat-pill--wrong {
        background: #2a181c;
        border-color: rgba(255, 107, 107, 0.72);
        color: #ffc0c0;
    }

    .stat-pill--total {
        background: #202534;
        border-color: rgba(122, 132, 160, 0.9);
        color: #e0e4f3;
    }

    /* Progress bar */
    .stProgress > div > div {
        background-color: #202636;
        border-radius: 999px;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent), var(--success));
        border-radius: 999px;
    }

    /* Tip box */
    .tip-box {
        font-size: 0.82rem;
        color: #8b92a0;
        margin-top: 0.95rem;
        line-height: 1.5;
    }

    /* Mobile tweaks */
    @media (max-width: 640px) {
        .question-card {
            padding: 1.3rem 1.1rem 1.1rem;
        }
        .app-header-card {
            padding: 1.4rem 1.3rem 1.2rem;
        }
        .german-word {
            font-size: 1.5rem;
        }
        .app-title {
            font-size: 1.6rem;
        }
        .qcols div[data-testid="stHorizontalBlock"],
        .btncols div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 0.8rem !important;
        }
        .btncols .stButton > button {
            width: 100% !important;
        }
        div.stRadio > div[role="radiogroup"] > label {
            padding: 0.8rem 0.95rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)

# -------------------
# Header
# -------------------
st.markdown(
    """
    <div class="app-header-card">
        <div class="app-title">Deutsch Trainer</div>
        <div class="app-tagline">
            A focused dark mode space to grow your vocabulary.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------
# Question card
# -------------------
st.markdown('<div class="question-card">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="question-header-label">Current word</div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="german-word">{word['german']}</div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="qcols">', unsafe_allow_html=True)
col_left, col_right = st.columns([2.2, 1.8])
with col_left:
    st.markdown('<div class="controls-row">', unsafe_allow_html=True)
    show_plural = st.checkbox("Show plural", value=True)
    show_example = st.checkbox("Show example", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if show_plural and word["plural"]:
        st.markdown(
            f'<div class="meta-info"><span class="meta-highlight">Plural</span>: {word["plural"]}</div>',
            unsafe_allow_html=True,
        )

    if show_example and word["example"]:
        st.markdown(
            """
            <div class="example-container">
                <div class="example-label">Example</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="example-text">{word["example"]}</div></div>',
            unsafe_allow_html=True,
        )

with col_right:
    st.markdown(
        """
        <div class="meta-info">
            🔤 <span class="meta-highlight">Vocabulary card</span><br/>
            Stay consistent and the words will stick.
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='answer-area'>", unsafe_allow_html=True)
st.markdown(
    "<div class='answer-label'>Select the correct English meaning:</div>",
    unsafe_allow_html=True,
)
choice = st.radio(
    "",
    options,
    key="answer_choice",
)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------
# Actions
# -------------------
st.markdown('<div class="button-row btncols">', unsafe_allow_html=True)
check_col, next_col = st.columns(2)

with check_col:
    with st.container():
        check_clicked = st.button(
            "Check answer",
            key="check_btn",
            type="primary",
            use_container_width=True,
        )

with next_col:
    with st.container():
        next_clicked = st.button(
            "Next word",
            key="next_btn",
            type="secondary",
            disabled=not st.session_state.answered_current_question,
            use_container_width=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# -------------------
# Check answer logic (unchanged functionality)
# -------------------
if check_clicked:
    selected = st.session_state.get("answer_choice")

    if selected == correct_answer:
        st.success("✅ Correct! Nice work.")
        st.session_state.correct += 1
    else:
        st.error(f"❌ Not quite. The correct answer is: {correct_answer}")
        st.session_state.wrong += 1

    st.session_state.answered_current_question = True

if next_clicked:
    setup_new_question()
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# -------------------
# Progress tracker
# -------------------
total_answered = st.session_state.correct + st.session_state.wrong
accuracy = (st.session_state.correct / total_answered) * 100 if total_answered else 0.0

st.markdown('<div class="progress-card">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="progress-header">
        <div class="progress-title">Session progress</div>
        <div class="progress-subtitle">
            {'Nice rhythm – keep going.' if total_answered else 'Answer your first question to begin.'}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.progress(accuracy / 100 if accuracy else 0.0)

st.markdown(
    f"""
    <div class="stat-row">
        <div class="stat-pill stat-pill--correct">✅ Correct: {st.session_state.correct}</div>
        <div class="stat-pill stat-pill--wrong">❌ Wrong: {st.session_state.wrong}</div>
        <div class="stat-pill stat-pill--total">📚 Total: {total_answered}</div>
        <div class="stat-pill">🎯 Accuracy: {accuracy:.1f}%</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="tip-box">
        You can extend your deck at any time by editing <code>vocab.csv</code>.
        New words will appear automatically in future questions.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
