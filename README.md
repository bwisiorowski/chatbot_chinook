# Chatbot bazy Chinook

Chatbot połączony z bazą Chinook (credits: https://github.com/lerocha/chinook-database).
Pytanie zamieniane jest na SQL przez lokalny model w Ollamie.
Zapytanie wykonywane jest na PostgreSQL, a wynik opisywany zwyłkym tekstem.
Bot pamięta kilka ostatnich pytań.

## Wymagania

- Docker
- Ollama
- Python 3.12+

## Uruchomienie

1. Skopiuj `.env.example` do `.env` i wpisz hasła (DB_RO_PASSWORD i DB_PASSWORD muszą być takie same)
2. `docker compose up -d` - baza z danymi i kontem tylko do odczytu
3. `ollama pull qwen2.5-coder:7b`
4. `pip install -r requirements.txt`
5. `streamlit run app.py` albo w terminalu `python cli.py`

## Struktura

- `app.py` - aplikacja w Streamlit
- `cli.py` - wersja w terminalu
- `chatbot/bot.py` - zamiana pytania na SQL i odpowiedź, pamięć chatbota
- `chatbot/database.py` - połączenie z bazą i sprawdzanie, czy SQL tylko czyta dane
- `chatbot/prompts.py` - prompty dla modelu
- `components/streamlit_ui.py` - elementy czatu w Streamlit
- `init-scripts/` - skrypty tworzące bazę przy pierwszym starcie
