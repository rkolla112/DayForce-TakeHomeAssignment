import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "employees.db"
DEPARTMENTS = ("Sales", "Marketing", "Engineering")
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
BLOCKED_SQL_KEYWORDS = (
    "ALTER",
    "ATTACH",
    "CREATE",
    "DELETE",
    "DETACH",
    "DROP",
    "INSERT",
    "PRAGMA",
    "REINDEX",
    "REPLACE",
    "UPDATE",
    "VACUUM",
)
