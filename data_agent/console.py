import random

from data_agent.config import DEPARTMENTS
from data_agent.database import format_results, run_query
from data_agent.llm import generate_sql, get_groq_client


def select_department() -> str:
    return random.choice(DEPARTMENTS)


def is_exit_command(value: str) -> bool:
    return value.strip().lower() in {"exit", "quit"}


def answer_question(question: str, department: str, client=None) -> tuple[str, str]:
    sql = generate_sql(question, department, client)
    result = run_query(sql, department)
    return sql, format_results(result)


def query_loop(department: str) -> None:
    client = None
    while True:
        try:
            question = input("\nAsk a question (or type 'exit'): ").strip()
        except EOFError:
            print("\nGoodbye!")
            return

        if is_exit_command(question):
            print("Goodbye!")
            return
        if not question:
            print("Please enter a question, or type 'exit' to quit.")
            continue

        try:
            client = client or get_groq_client()
            sql, formatted_results = answer_question(question, department, client)
            print("\nGenerated SQL:")
            print(sql)
            print("\nResults:")
            print(formatted_results)
        except Exception as exc:
            print(f"Error: {exc}")


def main() -> None:
    department = select_department()
    print(f"[INFO] Department selected: {department}")
    query_loop(department)
