import streamlit as st
import csv
import random

# -------------------
# Load vocabulary
# -------------------
vocab_file = "vocab.csv"
vocab = []

with open(vocab_file, encoding="utf-8-sig") as f:
    reader = csv.reader(f, delimiter=';')
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
    """Pick a new word and stable multiple‑choice options."""
    st.session_state.current_word = random.choice(vocab)
    word = st.session_state.current_word
    correct = word["english"]

    # Build pool of wrong answers
    wrong_answers = [w["english"] for w in vocab if w["english"] != correct]
    wrong_options = random.sample(wrong_answers, min(3, len(wrong_answers)))

    options = wrong_options + [correct]
    random.shuffle(options)

    st.session_state.correct_answer = correct
    st.session_state.options = options


# -------------------
# Initialize session state
# -------------------
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0

if "current_word" not in st.session_state or "options" not in st.session_state or "correct_answer" not in st.session_state:
    setup_new_question()

word = st.session_state.current_word
correct_answer = st.session_state.correct_answer
options = st.session_state.options

# -------------------
# App title
# -------------------
st.title("German Vocabulary Trainer with Progress Tracker")

# -------------------
# Show current word
# -------------------
st.subheader(f"German: {word['german']}")

# Checkboxes
show_plural = st.checkbox("Show plural?", value=True)
show_example = st.checkbox("Show example sentences?", value=True)

if show_plural and word["plural"]:
    st.write(f"Plural: {word['plural']}")

if show_example and word["example"]:
    st.write(f"Example: {word['example']}")

# -------------------
# Multiple-choice options
# -------------------
choice = st.radio(
    "Select the correct English meaning:",
    options,
    key="answer_choice",
)

# -------------------
# Check answer button
# -------------------
if st.button("Check Answer"):
    selected = st.session_state.get("answer_choice")

    if selected == correct_answer:
        st.success("✅ Correct!")
        st.session_state.correct += 1
    else:
        st.error(f"❌ Wrong. The correct answer is: {correct_answer}")
        st.session_state.wrong += 1

st.write("---")
if st.button("Next word"):
    setup_new_question()
    # Immediately rerun so the new word and options show up
    try:
        st.rerun()
    except AttributeError:
        # For older Streamlit versions
        st.experimental_rerun()

# -------------------
# Progress tracker
# -------------------
total_answered = st.session_state.correct + st.session_state.wrong
st.write(f"✅ Correct answers: {st.session_state.correct}")
st.write(f"❌ Wrong answers: {st.session_state.wrong}")
st.write(f"Total answered: {total_answered}")

if total_answered:
    accuracy = (st.session_state.correct / total_answered) * 100
    st.write(f"🎯 Accuracy: {accuracy:.1f}%")

st.info("Tip: You can add new words to vocab.csv any time. They will appear automatically in your practice!")