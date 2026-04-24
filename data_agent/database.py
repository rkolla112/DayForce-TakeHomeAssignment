import sqlite3
from dataclasses import dataclass
from pathlib import Path

from tabulate import tabulate

from data_agent.config import DB_PATH
from data_agent.sql_guard import validate_sql


@dataclass(frozen=True)
class QueryResult:
    columns: list[str]
    rows: list[tuple]


def run_query(sql: str, department: str, db_path: Path = DB_PATH) -> QueryResult:
    validate_sql(sql, department)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "CREATE TEMP TABLE Employee AS "
            "SELECT * FROM main.Employee WHERE Department = ?",
            (department,),
        )
        cursor = conn.execute(sql)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
    return QueryResult(columns=columns, rows=rows)


def format_results(result: QueryResult) -> str:
    if not result.rows:
        return "No results found for this department."
    return tabulate(result.rows, headers=result.columns, tablefmt="grid")
