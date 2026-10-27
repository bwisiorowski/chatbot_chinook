SQL_PROMPT = """You are a PostgreSQL expert. The database is the Chinook music store.
Schema:
{schema}

Rules:
1. Use ONLY tables and columns from the schema.
2. Return ONE SELECT query and nothing else (no comments, no markdown).
3. Write full table names (track.name, invoice_line.quantity), not aliases like T1, T2.
4. Text values in the database are in English, e.g. 'Brazil', 'Germany'.
5. Return names, not IDs: first_name and last_name for customers and employees,
   name or title for artists, albums, tracks and genres. Join the tables needed to get them.
6. When the question is about track length, include the length in the result as
   (track.milliseconds / 1000 * interval '1 second')::text, not raw milliseconds.
7. The question may refer to the earlier conversation (e.g. "and how many of them", "that artist").
   Use the conversation below to understand what it means.
8. If the question cannot be answered from this database, return only: NIE_DA_SIE

Earlier conversation:
{history}

Question: {question}
SQL:"""

FIX_PROMPT = """You are a PostgreSQL expert. Schema of the Chinook database:
{schema}

Earlier conversation:
{history}

Question: {question}
This query failed: {sql}
Error: {error}

Find the table or column from the error in the schema above and fix the query.
Write full table names, not aliases like T1, T2.
Return only the corrected SELECT query. It must be different from the failed one.
SQL:"""

ANSWER_PROMPT = """Odpowiedz krótko po polsku (maksymalnie 3 zdania), korzystając tylko z wyniku z bazy.
Liczby przepisuj dokładnie z wyniku. Nie dodawaj waluty ani danych, których w wyniku nie ma.
Czas w formacie GG:MM:SS zapisz słownie, np. 00:13:36 to 13 min 36 s.

Wcześniejsza rozmowa:
{history}

Pytanie: {question}
Zapytanie SQL: {sql}
Wynik z bazy: {result}
Odpowiedź:"""
