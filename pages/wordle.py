import streamlit as st

ANSWER = "pizza"
MAX_TURNS = 6

if "target" not in st.session_state:
    st.session_state.target = ANSWER
    st.session_state.guesses = []
    st.session_state.solved = False
    st.session_state.failed = False
    st.session_state.show_solved_dialog = False
    st.session_state.show_failed_dialog = False
    st.session_state.turns = 0
    st.session_state.guess_input = ""

st.title("Wordle")
st.write("Guess the next activity!")

def format_feedback(guess: str, target: str) -> str:
    feedback = []
    target_letters = list(target)

    # first pass for greens
    result = [None] * 5
    for i, letter in enumerate(guess):
        if letter == target[i]:
            result[i] = "green"
            target_letters[i] = None

    # second pass for yellows and grays
    for i, letter in enumerate(guess):
        if result[i] is not None:
            continue
        if letter in target_letters:
            result[i] = "yellow"
            target_letters[target_letters.index(letter)] = None
        else:
            result[i] = "gray"

    for i, letter in enumerate(guess):
        color = {
            "green": "#6aaa64",
            "yellow": "#c9b458",
            "gray": "#787c7e",
        }[result[i]]
        feedback.append(
            f"<span style='display:inline-block; margin:2px; width:50px; height:50px;"
            f" line-height:50px; text-align:center; font-weight:bold; color:white; background:{color};'>{letter.upper()}</span>"
        )

    return "".join(feedback)

def format_empty_row() -> str:
    return "".join(
        f"<span style='display:inline-block; margin:2px; width:50px; height:50px;"
        f" line-height:50px; text-align:center; font-weight:bold; color:white; background:#d3d6da;'>&nbsp;</span>"
        for _ in range(5)
    )

def render_board() -> str:
    rows = []
    for guess_text in st.session_state.guesses:
        rows.append(format_feedback(guess_text, st.session_state.target))
    for _ in range(MAX_TURNS - len(st.session_state.guesses)):
        rows.append(format_empty_row())

    board_html = "<div style='display:flex; flex-direction:column; align-items: center; gap:1px; margin:0; padding:0;'>"
    for row_html in rows:
        board_html += f"<div style='margin:0; padding:0;'>{row_html}</div>"
    board_html += "</div>"
    return board_html

@st.dialog("Solved!")
def show_solved_popup():
    tries = "try" if st.session_state.turns == 1 else "tries"
    st.write(f"Congratulations! You guessed the word in {st.session_state.turns} {tries}!")
    if st.button("Admire Puzzle", width="stretch"):
        st.session_state.show_solved_dialog = False
        st.rerun()

@st.dialog("Game Over...")
def show_failed_popup():
    st.write(f"Sorry, you've used all {MAX_TURNS} turns! The word was '{st.session_state.target.upper()}'.")
    if st.button("Try Again", width="stretch"):
        st.session_state.show_failed_dialog = False
        st.rerun()

def reset_game():
    st.session_state.target = ANSWER
    st.session_state.guesses = []
    st.session_state.solved = False
    st.session_state.failed = False
    st.session_state.show_solved_dialog = False
    st.session_state.show_failed_dialog = False
    st.session_state.turns = 0
    st.session_state.guess_input = ""

with st.bottom:
    with st.form("guess_form", clear_on_submit=True):
        is_input_disabled = st.session_state.solved or st.session_state.failed
        guess = st.text_input("Type your guess here", max_chars=5, placeholder="Enter a 5-letter word", disabled=is_input_disabled)
        submit = st.form_submit_button("Submit", use_container_width=True, disabled=is_input_disabled)
    if st.button("Restart", width="stretch"):
        reset_game()

if submit and not st.session_state.solved:
    guess_text = guess.strip().lower()
    if len(guess_text) != 5:
        st.warning("Please enter exactly 5 letters.")
    else:
        st.session_state.guesses.append(guess_text)
        st.session_state.turns += 1
        if guess_text == st.session_state.target:
            st.session_state.solved = True
            st.session_state.show_solved_dialog = True
        elif st.session_state.turns >= MAX_TURNS:
            st.session_state.failed = True
            st.session_state.show_failed_dialog = True

st.markdown(render_board(), unsafe_allow_html=True)

if st.session_state.solved and st.session_state.show_solved_dialog:
    show_solved_popup()
elif st.session_state.failed and st.session_state.show_failed_dialog:
    show_failed_popup()

