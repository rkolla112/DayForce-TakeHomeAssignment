# Data Agents NL2SQL Console App
Console-based Natural Language to SQL application for the provided `employees.db` SQLite database. The app uses Groq-hosted Llama to translate user questions into SQL, validates the generated SQL, executes it, and prints readable tabular results.

## Features
- Interactive terminal query loop
- Random department selection at startup
- Mandatory department guardrail for every query
- LLM-generated SQLite `SELECT` statements
- Support for employees, certifications, benefits, joins, and aggregations
- Defensive SQL validation before execution
- Pytest coverage for guardrail, real SQLite integration, CLI startup, and optional live Groq behavior

## Guardrail Design
On startup, the app randomly selects one department from `Sales`, `Marketing`, or `Engineering` and logs it:

```bash
[INFO] Department selected: Marketing
```

The selected department is enforced in three places:

1. Prompt instructions require the generated SQL to include `Employee.Department = '<selected department>'`.
2. `validate_sql()` rejects non-`SELECT` statements, multi-statement SQL, unsafe keywords, schema-qualified table access, missing `Employee` table usage, and missing department filters.
3. `run_query()` creates a temporary `Employee` table containing only the selected department before executing the generated SQL. This execution-time isolation prevents cross-department rows from being returned even if the generated predicate is too broad.

## Setup
Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your Groq API key:

```bash
GROQ_API_KEY=your_api_key_here
```

Optional model override:

```bash
GROQ_MODEL=llama-3.1-8b-instant
```

## Run

```bash
python app.py
```

Type `exit` or `quit` to stop the application.

## Test

```bash
pytest -q -m "not live"
```

The non-live tests do not call the Groq API. They cover:

- SQL cleanup and unsafe SQL rejection
- Required department filtering
- Execution-time guardrail enforcement against the real `employees.db`
- Employee, certification, and benefits queries against the real database
- Empty result formatting
- `python app.py` startup, department logging, prompt display, and clean exit through a subprocess

The live Groq integration test is included but skipped unless `GROQ_API_KEY` is set:

```bash
GROQ_API_KEY=your_api_key_here pytest -q -m live
```

That live test calls Groq, executes the generated SQL through the same guardrail path as the app, and verifies that other departments are not shown.

To run every test, including the live Groq test when `GROQ_API_KEY` is available:

```bash
pytest -q
```

## Example Questions

- Who are the software engineers?
- Which employees have an AWS certification?
- What is the average salary?
- List employees who started after 2023 and their certifications.
- Who has the highest remaining benefits balance?

## Architecture

```text
User input
  -> Groq LLM SQL generation
  -> SQL cleanup
  -> SQL validation
  -> SQLite execution with filtered temporary Employee table
  -> Tabulated console output
```

Key functions:

- `app.py` is the thin executable entry point.
- `data_agent/config.py` contains shared constants and paths.
- `data_agent/llm.py` builds prompts, calls Groq, and cleans SQL.
- `data_agent/sql_guard.py` applies SQL safety and guardrail checks.
- `data_agent/database.py` executes SQL against SQLite while isolating `Employee` rows to the selected department.
- `data_agent/console.py` handles startup, department selection, and the interactive query loop.

## Database Relationships

- `Certification.EmployeeId` -> `Employee.EmployeeId` (many-to-one; an employee may have zero or more certifications)
- `Benefits.EmployeeId` -> `Employee.EmployeeId` (many-to-one; an employee may have zero or more benefits records)

## AI Tooling Used

AI tool (such as ChatGPT) was used lightly (around 20%) for small suggestions, debugging, and clarifying requirements.
The overall design, implementation, and key logic—especially guardrail enforcement and system structure—were developed independently.

## Assumptions

- Only SQLite `SELECT` queries are allowed.
- Generated SQL must include the `Employee` table so the selected department can be enforced consistently.
- Evaluators will provide their own `GROQ_API_KEY` for running the app or live Groq integration test.
- The provided `employees.db` file remains in the project root.
