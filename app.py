import streamlit as st

from chatbot import ask
from components import streamlit_ui as ui

st.set_page_config(page_title="Chatbot bazy Chinook")
st.title("Chatbot bazy Chinook")

ui.init_chat()

if st.sidebar.button("Nowy czat"):
    ui.new_chat()

ui.show_messages()

question = ui.get_question()
if question:
    ui.add_message("user", question)

    with st.spinner("Szukam odpowiedzi w bazie..."):
        try:
            answer, sql = ask(question, st.session_state.history)
        except Exception as e:
            answer, sql = f"Error: {e}", None

    st.session_state.history.append((question, sql, answer))
    ui.add_message("assistant", answer, sql)
