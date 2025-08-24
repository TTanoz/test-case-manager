from datetime import datetime
from utils import get_case

def _latest_result_for_case(data, case_id):
    latest = None
    latest_ts = None
    for r in data.get("runs", []):
        r_time = r.get("executed_at")
        try:
            ts = datetime.fromisoformat(r_time) if r_time else None
        except Exception:
            ts = None
        for res in r.get("results", []):
            if res.get("case_id") == case_id:
                if latest is None or (ts and latest_ts and ts > latest_ts) or (ts and not latest_ts):
                    latest = res
                    latest_ts = ts
    return latest

def report_by_tag(data, tag):
    if not tag:
        return []
    tgt = str(tag).lower().strip()
    out = []
    for c in data.get("cases", []):
        tags = [str(t).lower() for t in c.get("tags", [])]
        if tgt in tags:
            latest = _latest_result_for_case(data, c.get("id"))
            last_str = latest.get("result") if latest else None
            out.append({
                "id": c.get("id"),
                "title": c.get("title"),
                "status": c.get("status", ""),
                "priority": c.get("priority", ""),
                "tags": c.get("tags", []),
                "last_result": last_str
            })
    return out

def report_flaky_candidates(data, last_n_runs=5):
    runs = sorted(data.get("runs", []), key=lambda r: r.get("executed_at", ""))[-last_n_runs:]
    history = {}  # case_id -> set(results)
    for r in runs:
        for res in r.get("results", []):
            cid = res.get("case_id")
            val = res.get("result")
            if cid is None or val is None:
                continue
            history.setdefault(cid, set()).add(val)

    flaky = []
    for cid, seen in history.items():
        if "pass" in seen and "fail" in seen:
            c = get_case(data, cid)
            flaky.append({
                "case_id": cid,
                "title": c.get("title") if c else "?",
                "seen": sorted(seen)
            })
    return flaky
