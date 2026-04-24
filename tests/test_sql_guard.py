import pytest

from data_agent.llm import clean_sql
from data_agent.sql_guard import validate_sql


def test_clean_sql_extracts_select_from_markdown():
    raw_sql = """
```sql
SELECT Name FROM Employee WHERE Department = 'Sales';
```
"""

    assert clean_sql(raw_sql) == "SELECT Name FROM Employee WHERE Department = 'Sales';"


def test_validate_sql_rejects_non_select_statement():
    with pytest.raises(ValueError, match="Only SELECT"):
        validate_sql("DELETE FROM Employee WHERE Department = 'Sales';", "Sales")


def test_validate_sql_rejects_multiple_statements():
    with pytest.raises(ValueError, match="Only one SQL statement"):
        validate_sql(
            "SELECT Name FROM Employee WHERE Department = 'Sales'; SELECT * FROM Employee;",
            "Sales",
        )


def test_validate_sql_rejects_missing_employee_table():
    with pytest.raises(ValueError, match="Employee table"):
        validate_sql(
            "SELECT CertificationName FROM Certification WHERE Department = 'Sales';",
            "Sales",
        )


def test_validate_sql_rejects_missing_department_filter():
    with pytest.raises(ValueError, match="Department guardrail"):
        validate_sql("SELECT Name FROM Employee;", "Sales")


def test_validate_sql_rejects_schema_qualified_employee_access():
    with pytest.raises(ValueError, match="Schema-qualified"):
        validate_sql("SELECT Name FROM main.Employee WHERE Department = 'Sales';", "Sales")
