import os
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from .database import UnsafeSQL, run_sql, schema
from .prompts import ANSWER_PROMPT, FIX_PROMPT, SQL_PROMPT

MEMORY_SIZE = 3

llm = ChatOllama(model=os.getenv("LLM_MODEL", "qwen2.5-coder:7b"), temperature=0, num_ctx=8192)


def make_chain(template):
    return PromptTemplate.from_template(template) | llm | StrOutputParser()


sql_chain = make_chain(SQL_PROMPT)
fix_chain = make_chain(FIX_PROMPT)
answer_chain = make_chain(ANSWER_PROMPT)


def format_history(history):
    if not history:
        return "(none)"
    parts = []
    for question, sql, answer in history[-MEMORY_SIZE:]:
        parts.append(f"Q: {question}\nSQL: {sql or '-'}\nA: {answer}")
    return "\n\n".join(parts)


def clean_sql(text):
    match = re.search(r"```(?:sql)?(.*?)```", text, re.S | re.I)
    if match:
        text = match.group(1)
    return text.split(";")[0].strip()


def ask(question, history):
    """Odpowiada na pytanie - struktura history (pytanie, SQL, odpowiedź)"""
    past = format_history(history)

    raw = sql_chain.invoke({"schema": schema, "history": past, "question": question})
    if "NIE_DA_SIE" in raw.upper():
        return "Baza nie obejmuje tego zakresu", None

    sql = clean_sql(raw)
    try:
        result = run_sql(sql)
    except UnsafeSQL as e:
        return f"Zapytanie odrzucone: {e}", sql
    except Exception as e:
        error = str(e).splitlines()[0]
        sql = clean_sql(fix_chain.invoke(
            {"schema": schema, "history": past, "question": question, "sql": sql, "error": error}))
        try:
            result = run_sql(sql)
        except Exception as e:
            return f"Zapytanie się nie powiodło: {str(e).splitlines()[0]}", sql

    if not result or result.strip() == "[]":
        return "Brak takich danych", sql

    answer = answer_chain.invoke(
        {"history": past, "question": question, "sql": sql, "result": result[:3000]})
    return answer.strip(), sql
