import sqlite3
import random
import os
import re
from dotenv import load_dotenv
from tabulate import tabulate
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DEPARTMENTS = ["Sales", "Marketing", "Engineering"]
department = random.choice(DEPARTMENTS)

print(f"[INFO] Department selected: {department}")

DB_PATH = "employees.db"


def generate_sql(question):
    prompt = f"""
You are an expert SQLite SQL generator.

Return ONLY ONE valid SQLite SELECT query. Prefer human-readable columns like Employee.Name, Employee.Role, Certification.CertificationName, Benefits.BenefitsPackage, and Benefits.RemainingBalance instead of only IDs. Use DISTINCT when joins may create duplicates.
Do NOT use markdown.
Do NOT explain.
Do NOT give alternatives.
Do NOT wrap SQL in ```.

Database schema:
Employee(EmployeeId, Name, Department, Role, EmploymentStartDate, SalaryAmount, YearlyBonusAmount)
Certification(CertificationId, EmployeeId, CertificationName, DateAchieved)
Benefits(BenefitId, EmployeeId, BenefitsPackage, RemainingBalance)

Rules:
- Only generate SELECT queries.
- Always use Employee table when filtering department.
- Always filter by Employee.Department = '{department}'.
- Use table aliases if needed.
- Never return data outside department '{department}'.

User question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()
    return clean_sql(sql)


def clean_sql(sql):
    sql = sql.replace("```sql", "").replace("```", "").strip()

    match = re.search(r"SELECT[\s\S]*?;", sql, re.IGNORECASE)
    if match:
        sql = match.group(0)

    if not sql.endswith(";"):
        sql += ";"

    return sql


def validate_sql(sql):
    blocked = ["DELETE", "UPDATE", "INSERT", "DROP", "ALTER", "CREATE", "REPLACE"]
    upper_sql = sql.upper()

    if not upper_sql.strip().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    for word in blocked:
        if word in upper_sql:
            raise ValueError(f"Unsafe SQL detected: {word}")
        if "DEPARTMENT" not in upper_sql:
            raise ValueError("Department guardrail missing from SQL.")

    return True


def run_query(sql):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = ["Average Salary"] if "AVG" in sql.upper() else [desc[0] for desc in cursor.description]

    conn.close()

    if not rows:
       print("No results found for this department.")
    else:
        print(tabulate(rows, headers=columns, tablefmt="grid"))


while True:
    question = input("\nAsk a question (or type 'exit'): ")

    if question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    try:
        sql = generate_sql(question)

        print("\nGenerated SQL:")
        print(sql)

        validate_sql(sql)

        print("\nResults:")
        run_query(sql)

    except Exception as e:
        print(f"Error: {e}")