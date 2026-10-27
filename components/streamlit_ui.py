from pathlib import Path

import streamlit as st

END_WORDS = ("koniec", "exit", "quit")
STYLE = Path(__file__).parent / "style.css"


def load_style():
    st.html(STYLE)


def init_chat():
    if "messages" not in st.session_state:
        new_chat()


def new_chat():
    st.session_state.messages = []
    st.session_state.history = []
    st.session_state.ended = False


def show_message(msg):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sql"):
            with st.expander("Treść zapytania SQL"):
                st.code(msg["sql"], language="sql")


def show_messages():
    for msg in st.session_state.messages:
        show_message(msg)


def add_message(role, content, sql=None):
    msg = {"role": role, "content": content, "sql": sql}
    st.session_state.messages.append(msg)
    show_message(msg)


def get_question():
    ended = st.session_state.ended
    if ended:
        st.info("Czat zakończony")

    question = st.chat_input("Zadaj pytanie", disabled=ended)
    if question and question.strip().lower() in END_WORDS:
        st.session_state.ended = True
        st.rerun()
    return question


def new_chat_button():
    with st.container(horizontal_alignment="center"):
        if st.button("Nowy czat", key="new_chat"):
            new_chat()
            st.rerun()


def show_footer():
    st.html('<div class="footer">© Bartosz Wisiorowski</div>')
