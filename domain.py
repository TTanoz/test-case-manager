from storage import save_to_file
from utils import get_suite, get_case

# -------- Suites --------
def add_suite(data, name, description, auto_save=True):
    suite_id = data.get("idx", 1)
    suite = {"id": suite_id, "name": name, "description": description, "cases": []}
    data.setdefault("suites", []).append(suite)
    data["idx"] = suite_id + 1
    if auto_save:
        save_to_file(data)
    return suite_id

def list_suites(data):
    return [
        (s.get("id"), s.get("name"), len(s.get("cases", [])))
        for s in data.get("suites", [])
    ]

def suite_details(data, suite_id):
    suite = get_suite(data, suite_id)
    if not suite:
        return None
    details = {
        "id": suite.get("id"),
        "name": suite.get("name"),
        "description": suite.get("description"),
        "cases": []
    }
    for cid in suite.get("cases", []):
        c = get_case(data, cid)
        if c:
            details["cases"].append({
                "id": c.get("id"),
                "title": c.get("title"),
                "status": c.get("status", "")
            })
        else:
            details["cases"].append({"id": cid, "title": None, "status": None})
    return details

def connect_case_to_suite(data, case_id, suite_id, auto_save=True):
    suite = get_suite(data, suite_id)
    if not suite:
        raise ValueError(f"Suite {suite_id} not found")
    if not get_case(data, case_id):
        raise ValueError(f"Case {case_id} not found")
    suite.setdefault("cases", [])
    if case_id not in suite["cases"]:
        suite["cases"].append(case_id)
        if auto_save:
            save_to_file(data)
        return True
    return False

# -------- Cases --------
def add_case(data, title, priority, tags, steps, auto_save=True):
    cases = data.setdefault("cases", [])
    new_id = (cases[-1].get("id", 100) + 1) if cases else 101
    case = {
        "id": new_id,
        "title": title,
        "status": "active",
        "priority": priority,
        "tags": tags,
        "steps": steps
    }
    cases.append(case)
    if auto_save:
        save_to_file(data)
    return new_id

def search_cases(data, key):
    needle = key.lower().strip()
    results = []
    for c in data.get("cases", []):
        title = str(c.get("title", "")).lower()
        tags = [str(t).lower() for t in c.get("tags", [])]
        if needle in title or needle in tags:
            results.append(c)
    return results

def list_cases(data, filters=None):
    cases = data.get("cases", [])
    f = filters or {}
    f_status = f.get("status")
    f_priority = f.get("priority")
    f_tag = (f.get("tag") or "").strip() or None
    q = (f.get("q") or f.get("title_contains") or "").lower().strip() or None

    def matches(c):
        if f_status and c.get("status") != f_status: return False
        if f_priority and c.get("priority") != f_priority: return False
        if f_tag and f_tag not in c.get("tags", []): return False
        if q and q not in str(c.get("title", "")).lower(): return False
        return True

    return [c for c in cases if matches(c)]