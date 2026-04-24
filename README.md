# Data Agents — NL2SQL Application

## Overview
This project is a console-based Natural Language to SQL (NL2SQL) application that allows users to ask questions in plain English and dynamically generates SQL queries to retrieve results from a SQLite database.

The system uses an LLM (Groq - Llama 3.1) to translate user queries into SQL and executes them against the provided `employees.db`.

## Features

- Natural language query interface
- Dynamic SQL generation using LLM
- Support for joins, aggregations, and filters
- Console-based interactive loop
- Clean tabular output formatting

## Guardrail Enforcement (Key Requirement)

At application startup:
- A department is randomly selected (`Sales`, `Marketing`, or `Engineering`)
- All queries are restricted to that department

This is enforced in:
1. Prompt design (LLM instructed to include department filter)
2. SQL validation layer (ensures `Department` is always present)

This prevents cross-department data leakage.

## Architecture
User Input → LLM (Groq) → SQL Generation → Validation → SQLite Execution → Output
### Components:
- `generate_sql()` → Uses LLM to convert natural language into SQL
- `validate_sql()` → Ensures only safe SELECT queries are executed
- `run_query()` → Executes SQL against SQLite database
- Guardrail enforcement → Ensures department filtering

## Technologies Used

- Python
- SQLite
- Groq API (Llama 3.1 model)
- Tabulate (for output formatting)
- dotenv (for API key management)

## Setup Instructions

### 1. Clone or unzip the project

### 2. Create virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add API Key
Create a .env file:
GROQ_API_KEY=your_api_key_here

Running the Application
python app.py

## Example Queries

* Who are the software engineers?
* Which employees have certifications?
* What is the average salary?
* Who has the highest remaining benefits balance?
* List employees who started after 2023 and their certifications


## Assumptions

* Only SELECT queries are allowed
* Department filtering is mandatory
* SQLite is used as the database
* LLM may not always be perfect, so validation is applied

## Notes

* Focus was on correctness, safety, and guardrail enforcement
* The system is designed to be simple, readable, and extensible
