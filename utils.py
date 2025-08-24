from datetime import datetime

def iso_now():
    return datetime.now().isoformat(timespec="seconds")

def get_suite(data, suite_id):
    for s in data.get("suites", []):
        if s.get("id") == suite_id:
            return s
    return None

def get_case(data, case_id):
    for c in data.get("cases", []):
        if c.get("id") == case_id:
            return c
    return None

def ensure_next_run_id(data):
    if "next_run_id" not in data or not isinstance(data["next_run_id"], int):
        runs = data.get("runs", [])
        if runs:
            last = max(r.get("id", 9000) for r in runs)
            data["next_run_id"] = last + 1
        else:
            data["next_run_id"] = 9001