from data_agent.llm import build_prompt


def test_build_prompt_documents_relationship_cardinality_and_optionality():
    prompt = build_prompt("Which employees have benefits?", "Engineering")

    assert (
        "Certification.EmployeeId -> Employee.EmployeeId "
        "(many-to-one; an employee may have zero or more certifications)"
    ) in prompt
    assert (
        "Benefits.EmployeeId -> Employee.EmployeeId "
        "(many-to-one; an employee may have zero or more benefits records)"
    ) in prompt
