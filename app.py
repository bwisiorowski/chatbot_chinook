import streamlit as st

from chatbot import ask
from components import streamlit_ui as ui

st.set_page_config(page_title="Chatbot bazy Chinook")
ui.load_style()
st.title("Chatbot bazy Chinook", text_alignment="center")

ui.init_chat()
ui.show_messages()

with st.bottom:
    with st.container():
        question = ui.get_question()
    ui.new_chat_button()

ui.show_footer()

if question:
    ui.add_message("user", question)

    with st.spinner("Szukam odpowiedzi w bazie..."):
        try:
            answer, sql = ask(question, st.session_state.history)
        except Exception as e:
            answer, sql = f"Error: {e}", None

    st.session_state.history.append((question, sql, answer))
    ui.add_message("assistant", answer, sql)