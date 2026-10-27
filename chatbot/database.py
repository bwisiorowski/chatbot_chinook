import os

import sqlglot
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlglot import exp

load_dotenv()

MAX_ROWS = 200

TABLES = ["artist", "album", "track", "genre", "media_type", "customer",
          "employee", "invoice", "invoice_line", "playlist", "playlist_track"]

FORBIDDEN = (exp.Insert, exp.Update, exp.Delete, exp.Merge, exp.Drop, exp.Create,
             exp.Alter, exp.Copy, exp.Set, exp.Command, exp.TruncateTable)

url = URL.create(
    "postgresql+psycopg2",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "chinook"),
)
db = SQLDatabase(create_engine(url), include_tables=TABLES, sample_rows_in_table_info=2)
schema = db.get_table_info()


class UnsafeSQL(ValueError):
    pass


def check_sql(sql):
    try:
        statements = [s for s in sqlglot.parse(sql, read="postgres") if s]
    except sqlglot.errors.SqlglotError:
        raise UnsafeSQL("error SQL")

    if len(statements) != 1 or not isinstance(statements[0], exp.Query):
        raise UnsafeSQL("dozwolone jest tylko jedno zapytanie SELECT")
    if statements[0].find(*FORBIDDEN):
        raise UnsafeSQL("zapytanie zmienia dane")
    if any(s.args.get("into") for s in statements[0].find_all(exp.Select)):
        raise UnsafeSQL("SELECT INTO jest zabronione")


def run_sql(sql):
    check_sql(sql)
    return db.run(f"SELECT * FROM ({sql}) AS t LIMIT {MAX_ROWS}", include_columns=True)
