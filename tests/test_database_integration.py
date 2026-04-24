from data_agent.database import format_results, run_query


def test_run_query_filters_employee_table_at_execution_time_against_real_db():
    sql = "SELECT Name, Department FROM Employee WHERE Department = 'Engineering' OR 1 = 1;"

    result = run_query(sql, "Engineering")

    assert result.rows
    assert {row[1] for row in result.rows} == {"Engineering"}
    assert len(result.rows) == 34


def test_run_query_supports_certification_join_against_real_db():
    sql = """
SELECT Employee.Name, Employee.Department, Certification.CertificationName
FROM Employee
JOIN Certification ON Certification.EmployeeId = Employee.EmployeeId
WHERE Employee.Department = 'Marketing';
"""

    result = run_query(sql, "Marketing")

    assert result.rows
    assert {row[1] for row in result.rows} == {"Marketing"}


def test_run_query_supports_benefits_join_against_real_db():
    sql = """
SELECT Employee.Name, Employee.Department, Benefits.BenefitsPackage, Benefits.RemainingBalance
FROM Employee
JOIN Benefits ON Benefits.EmployeeId = Employee.EmployeeId
WHERE Employee.Department = 'Sales'
ORDER BY Benefits.RemainingBalance DESC
LIMIT 5;
"""

    result = run_query(sql, "Sales")

    assert result.rows
    assert len(result.rows) == 5
    assert {row[1] for row in result.rows} == {"Sales"}
    assert result.rows == sorted(result.rows, key=lambda row: row[3], reverse=True)


def test_format_results_handles_empty_result_set_from_real_db():
    sql = "SELECT Name FROM Employee WHERE Department = 'Sales' AND Name = 'Not A Real Employee';"

    result = run_query(sql, "Sales")

    assert format_results(result) == "No results found for this department."
