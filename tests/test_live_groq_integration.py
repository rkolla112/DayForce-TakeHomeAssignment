import os

import pytest

from data_agent.console import answer_question


pytestmark = pytest.mark.live


@pytest.mark.skipif(
    not os.getenv("GROQ_API_KEY"),
    reason="Set GROQ_API_KEY to run the live Groq integration test.",
)
def test_live_groq_generates_sql_and_returns_guarded_results():
    sql, formatted_results = answer_question("List employee names and roles", "Engineering")

    assert "SELECT" in sql.upper()
    assert "DEPARTMENT" in sql.upper()
    assert "Engineering" in sql
    assert "No results found" in formatted_results or "Engineering" in formatted_results
    assert "Sales" not in formatted_results
    assert "Marketing" not in formatted_results
