from chatbot import ask

print("Chatbot bazy danych Chinook - aby zakończyć sesję napisz 'koniec'\n")

history = []

while True:
    question = input("Ty: ").strip()
    if not question:
        continue
    if question.lower() in ("koniec", "exit", "quit"):
        break
    if question.lower() == "nowy":
        history = []
        print("Zaczynam nowy czat\n")
        continue

    try:
        answer, sql = ask(question, history)
    except Exception as e:
        print(f"Error: {e}\n")
        continue

    if sql:
        print(f"SQL: {sql}")
    print(f"Bot: {answer}\n")
    history.append((question, sql, answer))
