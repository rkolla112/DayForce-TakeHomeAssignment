import os
import re

from data_agent.config import MODEL


def get_groq_client():
    from dotenv import load_dotenv
    from groq import Groq

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a .env file or export it before running."
        )
    return Groq(api_key=api_key)


def build_prompt(question: str, department: str) -> str:
    return f"""
You are an expert SQLite SQL generator.

Return ONLY ONE valid SQLite SELECT query.
Do NOT use markdown.
Do NOT explain.
Do NOT give alternatives.
Do NOT wrap SQL in backticks.

Database schema:
Employee(EmployeeId, Name, Department, Role, EmploymentStartDate, SalaryAmount, YearlyBonusAmount)
Certification(CertificationId, EmployeeId, CertificationName, DateAchieved)
Benefits(BenefitId, EmployeeId, BenefitsPackage, RemainingBalance)

Relationships:
Certification.EmployeeId = Employee.EmployeeId
Benefits.EmployeeId = Employee.EmployeeId

Rules:
- Only generate SELECT queries.
- Always include the Employee table in FROM or JOIN.
- Always filter by Employee.Department = '{department}'.
- Prefer human-readable columns like Employee.Name, Employee.Role, Certification.CertificationName, Benefits.BenefitsPackage, and Benefits.RemainingBalance instead of only IDs.
- Use DISTINCT when joins may create duplicate employees.
- Never return data outside department '{department}'.

User question:
{question}
""".strip()


def generate_sql(question: str, department: str, client=None) -> str:
    client = client or get_groq_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": build_prompt(question, department)}],
        temperature=0,
    )
    return clean_sql(response.choices[0].message.content)


def clean_sql(sql: str) -> str:
    sql = sql.replace("```sql", "").replace("```", "").strip()
    match = re.search(r"\bSELECT\b[\s\S]*?;", sql, re.IGNORECASE)
    if match:
        sql = match.group(0)
    if not sql.endswith(";"):
        sql += ";"
    return sql
