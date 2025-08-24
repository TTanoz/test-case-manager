# Test Case Manager

A simple, CLI-based Test Case Manager built in Python.  
This project lets you manage **test suites**, **test cases**, **test runs**, and generate reports such as **tag-based summaries** and **flaky candidate detection**.

---

## Features
- Add, search, and list test suites and cases.
- Record test runs with results for each case.
- Summarize runs and calculate pass/fail statistics.
- Generate reports for:
  - Cases filtered by tags.
  - Flaky test detection (cases with both pass and fail results).

---

## Installation

```bash
git clone https://github.com/<your-username>/test-case-manager.git
cd test-case-manager
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

Run the CLI:
```bash
python cli.py
```

---

## Run Tests

Make sure you have `pytest` installed, then:
```bash
pytest
```

---

## Project Structure
```
test-case-manager/
├─ cli.py
├─ domain.py
├─ reports.py
├─ runs.py
├─ storage.py
├─ utils.py
├─ tests/
│  ├─ test_storage.py
│  ├─ test_domain_cases_suites.py
│  └─ test_runs_and_reports.py
├─ pytest.ini
├─ requirements.txt
└─ README.md
```

---

## License
Licensed under the [MIT License](./LICENSE).
