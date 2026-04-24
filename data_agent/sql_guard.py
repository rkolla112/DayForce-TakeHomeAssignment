import re

from data_agent.config import BLOCKED_SQL_KEYWORDS


def validate_sql(sql: str, department: str) -> None:
    normalized_sql = sql.strip()
    upper_sql = normalized_sql.upper()

    if not upper_sql.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    sql_without_trailing_semicolon = (
        normalized_sql[:-1] if normalized_sql.endswith(";") else normalized_sql
    )
    if ";" in sql_without_trailing_semicolon:
        raise ValueError("Only one SQL statement is allowed.")

    for keyword in BLOCKED_SQL_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            raise ValueError(f"Unsafe SQL detected: {keyword}")

    if re.search(r"\bmain\s*\.", normalized_sql, re.IGNORECASE):
        raise ValueError("Schema-qualified table access is not allowed.")

    if not re.search(
        r"\b(?:FROM|JOIN)\s+[`\"[]?Employee[`\"\]]?\b",
        normalized_sql,
        re.IGNORECASE,
    ):
        raise ValueError("Generated SQL must include the Employee table.")

    department_literal = re.escape(department)
    if not re.search(
        rf"\bDepartment\b\s*=\s*['\"]{department_literal}['\"]",
        normalized_sql,
        re.IGNORECASE,
    ):
        raise ValueError("Department guardrail missing from SQL.")
