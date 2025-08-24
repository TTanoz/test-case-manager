from storage import save_to_file
from utils import iso_now, get_suite, get_case, ensure_next_run_id

def create_run(data, suite_id, auto_save=True):
    suite = get_suite(data, suite_id)
    if not suite:
        raise ValueError(f"Suite {suite_id} not found")
    ensure_next_run_id(data)
    run_id = data["next_run_id"]
    run = {
        "id": run_id,
        "suite_id": suite_id,
        "executed_at": iso_now(),
        "results": []
    }
    data.setdefault("runs", []).append(run)
    data["next_run_id"] = run_id + 1
    if auto_save:
        save_to_file(data)
    return run_id

def add_run_result(data, run_id, case_id, result, notes="", auto_save=True):
    valid = {"pass", "fail", "blocked", "skip"}
    if result not in valid:
        raise ValueError(f"Invalid result: {result}")

    run = next((r for r in data.get("runs", []) if r.get("id") == run_id), None)
    if not run:
        raise ValueError(f"Run {run_id} not found")

    suite = get_suite(data, run.get("suite_id"))
    if not suite:
        raise ValueError("Run’s suite missing")
    if case_id not in suite.get("cases", []):
        raise ValueError(f"Case {case_id} not linked to suite {suite.get('id')}")
    if not get_case(data, case_id):
        raise ValueError(f"Case {case_id} not found in data")

    updated = False
    for res in run.get("results", []):
        if res.get("case_id") == case_id:
            res["result"] = result
            res["notes"] = notes
            updated = True
            break
    if not updated:
        run["results"].append({"case_id": case_id, "result": result, "notes": notes})

    if auto_save:
        save_to_file(data)

def run_summary(data, run_id):
    run = next((r for r in data.get("runs", []) if r.get("id") == run_id), None)
    if not run:
        raise ValueError(f"Run {run_id} not found")

    results = run.get("results", [])
    total = len(results)
    counts = {"pass": 0, "fail": 0, "blocked": 0, "skip": 0}
    for res in results:
        key = res.get("result", "skip")
        counts[key] = counts.get(key, 0) + 1

    return {
        "run_id": run_id,
        "suite_id": run.get("suite_id"),
        "executed_at": run.get("executed_at"),
        "total": total,
        "counts": counts
    }