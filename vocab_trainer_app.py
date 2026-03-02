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
# Initialize session state
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
# Global styling (CSS)
# -------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background: radial-gradient(circle at top left, #f2f6ff 0, #f7f7fb 45%, #fdfdfd 100%);
    }

    .main {
        background-color: transparent;
    }

    .app-wrapper {
        max-width: 720px;
        margin: 0 auto;
        padding: 1.5rem 1rem 3rem;
    }

    @media (min-width: 768px) {
        .app-wrapper {
            padding: 2.5rem 0 3.5rem;
        }
    }

    .app-header-card {
        background: linear-gradient(135deg, #4f9cff, #79d2ff);
        border-radius: 18px;
        padding: 1.5rem 1.75rem;
        color: white;
        box-shadow: 0 14px 35px rgba(37, 97, 192, 0.35);
        margin-bottom: 1.75rem;
    }

    .app-title {
        font-size: 1.85rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 0.25rem;
    }

    .app-tagline {
        font-size: 0.95rem;
        font-weight: 400;
        opacity: 0.9;
    }

    .question-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 1.5rem 1.4rem 1.2rem;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
        margin-bottom: 1.25rem;
        border: 1px solid rgba(148, 163, 184, 0.12);
    }

    .question-header-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #6b7280;
        margin-bottom: 0.3rem;
    }

    .german-word {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.45rem;
    }

    .meta-info {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 0.15rem;
    }

    .meta-highlight {
        font-weight: 500;
        color: #2563eb;
    }

    .example-text {
        font-size: 0.9rem;
        color: #4b5563;
        margin-top: 0.15rem;
    }

    .controls-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin-top: 0.35rem;
        margin-bottom: 0.4rem;
    }

    .stCheckbox > label, .stCheckbox span {
        font-size: 0.85rem;
        color: #4b5563;
    }

    /* Answer options styled as cards */
    .answer-area > div {
        margin-top: 0.35rem;
    }

    .answer-label {
        font-size: 0.9rem;
        color: #374151;
        margin-bottom: 0.35rem;
        font-weight: 500;
    }

    div.stRadio > div[role="radiogroup"] {
        gap: 0.5rem;
    }

    div.stRadio > div[role="radiogroup"] > label {
        border-radius: 12px;
        padding: 0.55rem 0.85rem;
        border: 1px solid rgba(148, 163, 184, 0.5);
        background: #f9fafb;
        display: flex;
        align-items: center;
        transition: all 0.16s ease-out;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }

    div.stRadio > div[role="radiogroup"] > label:hover {
        border-color: #2563eb;
        background: #eff6ff;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.12);
        transform: translateY(-1px);
    }

    div.stRadio > div[role="radiogroup"] > label div[role="radio"] {
        margin-right: 0.5rem;
    }

    /* Selected state */
    div.stRadio > div[role="radiogroup"] > label[data-checked="true"],
    div.stRadio > div[role="radiogroup"] > label:has(input:checked) {
        border-color: #2563eb;
        background: #e0edff;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.2);
    }

    /* Buttons */
    .button-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin-top: 0.8rem;
        margin-bottom: 0.2rem;
    }

    .stButton > button {
        border-radius: 999px !important;
        padding: 0.5rem 1.3rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.16s ease-out !important;
    }

    .primary-btn > button {
        background: linear-gradient(135deg, #2563eb, #0ea5e9) !important;
        color: #ffffff !important;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.35) !important;
    }

    .primary-btn > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(37, 99, 235, 0.45) !important;
    }

    .secondary-btn > button {
        background: #f3f4f6 !important;
        color: #111827 !important;
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.08) !important;
    }

    .secondary-btn > button:hover {
        background: #e5e7eb !important;
        transform: translateY(-1px);
    }

    .secondary-btn > button:disabled {
        opacity: 0.5;
        cursor: not-allowed !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* Feedback messages */
    .stAlert {
        border-radius: 12px;
    }

    .stAlert-success {
        background-color: #ecfdf3 !important;
        border-left: 4px solid #22c55e !important;
    }

    .stAlert-error {
        background-color: #fef2f2 !important;
        border-left: 4px solid #f87171 !important;
    }

    /* Progress section */
    .progress-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.1rem 1.4rem 1.2rem;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
        border: 1px solid rgba(148, 163, 184, 0.16);
        margin-top: 0.9rem;
    }

    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.45rem;
    }

    .progress-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #111827;
    }

    .progress-subtitle {
        font-size: 0.8rem;
        color: #6b7280;
    }

    .stat-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem 1.2rem;
        margin-top: 0.45rem;
        font-size: 0.88rem;
        color: #4b5563;
    }

    .stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.15rem 0.65rem;
        border-radius: 999px;
        background: #f3f4f6;
        font-size: 0.78rem;
        color: #374151;
    }

    .stat-pill--correct {
        background: #dcfce7;
        color: #166534;
    }

    .stat-pill--wrong {
        background: #fee2e2;
        color: #b91c1c;
    }

    .stat-pill--total {
        background: #e5e7eb;
        color: #111827;
    }

    /* Progress bar */
    .stProgress > div > div {
        background-color: #e5edff;
        border-radius: 999px;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #22c55e, #4ade80);
        border-radius: 999px;
    }

    /* Tip box */
    .tip-box {
        font-size: 0.82rem;
        color: #6b7280;
        margin-top: 0.9rem;
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
            Build your vocabulary one focused question at a time.
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

col_left, col_right = st.columns([2.2, 1.8])
with col_left:
    # Example / plural info toggles
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
            f'<div class="example-text">{word["example"]}</div>',
            unsafe_allow_html=True,
        )

with col_right:
    st.markdown(
        f"""
        <div class="meta-info">
            🔤 Type: <span class="meta-highlight">Vocabulary</span><br/>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
st.markdown('<div class="button-row">', unsafe_allow_html=True)
check_col, next_col = st.columns(2)

with check_col:
    with st.container():
        check_clicked = st.button("Check answer", key="check_btn")

with next_col:
    with st.container():
        next_clicked = st.button(
            "Next word",
            key="next_btn",
            disabled=not st.session_state.answered_current_question,
        )

st.markdown("</div>", unsafe_allow_html=True)

# -------------------
# Check answer logic (unchanged core behaviour, just styled feedback)
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
        <div class="progress-subtitle">{'Keep going!' if total_answered else 'Answer your first question to begin.'}</div>
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
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="tip-box">
        Pro tip: you can add new words to <code>vocab.csv</code> at any time – they will appear automatically in your next practice session.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
