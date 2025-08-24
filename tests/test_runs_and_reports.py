import storage
from domain import add_suite, add_case, connect_case_to_suite
from runs import create_run, add_run_result, run_summary
from reports import report_by_tag, report_flaky_candidates

def setup_basic_data(tmp_path):
    storage.DATA_PATH = tmp_path / "data.json"
    data = storage.DEFAULT_DATA.copy()
    sid = add_suite(data, "Login", "Auth", auto_save=False)
    c1 = add_case(data, "Valid login", "P2", ["smoke","login"], [], auto_save=False)
    c2 = add_case(data, "Invalid login", "P2", ["negative","login"], [], auto_save=False)
    connect_case_to_suite(data, c1, sid, auto_save=False)
    connect_case_to_suite(data, c2, sid, auto_save=False)
    return data, sid, c1, c2

def test_create_run_and_add_results(tmp_path):
    data, sid, c1, c2 = setup_basic_data(tmp_path)
    rid = create_run(data, sid, auto_save=False)
    add_run_result(data, rid, c1, "pass", auto_save=False)
    add_run_result(data, rid, c2, "fail", "Server 500", auto_save=False)

    summary = run_summary(data, rid)
    assert summary["total"] == 2
    assert summary["counts"]["pass"] == 1
    assert summary["counts"]["fail"] == 1

def test_reports(tmp_path):
    data, sid, c1, c2 = setup_basic_data(tmp_path)

    # First run
    r1 = create_run(data, sid, auto_save=False)
    add_run_result(data, r1, c1, "pass", auto_save=False)
    add_run_result(data, r1, c2, "fail", auto_save=False)

    # Second run flips one result to make flaky
    r2 = create_run(data, sid, auto_save=False)
    add_run_result(data, r2, c2, "pass", auto_save=False)

    by_tag = report_by_tag(data, "login")
    ids = sorted([row["id"] for row in by_tag])
    assert ids == sorted([c1, c2])

    flaky = report_flaky_candidates(data, last_n_runs=5)
    # c2 had both pass and fail across last runs
    flaky_ids = [row["case_id"] for row in flaky]
    assert c2 in flaky_ids
