import storage
from domain import add_suite, list_suites, add_case, connect_case_to_suite, suite_details

def test_add_suite_and_case_connect(tmp_path):
    storage.DATA_PATH = tmp_path / "data.json"
    data = storage.DEFAULT_DATA.copy()

    sid = add_suite(data, "Login Suite", "Auth tests", auto_save=True)
    assert sid == 1
    assert list_suites(data) == [(1, "Login Suite", 0)]

    cid = add_case(data, "Valid login", "P2", ["smoke", "login"], [{"no":1,"action":"open","expected":"ok"}], auto_save=True)
    assert cid == 101

    changed = connect_case_to_suite(data, cid, sid, auto_save=True)
    assert changed is True

    det = suite_details(data, sid)
    assert det["id"] == 1
    assert det["cases"][0]["title"] == "Valid login"

def test_connect_case_twice_is_idempotent(tmp_path):
    storage.DATA_PATH = tmp_path / "data.json"
    data = storage.DEFAULT_DATA.copy()
    sid = add_suite(data, "Core", "Core suite", auto_save=False)
    cid = add_case(data, "Case A", "P3", ["core"], [], auto_save=False)

    first = connect_case_to_suite(data, cid, sid, auto_save=False)
    second = connect_case_to_suite(data, cid, sid, auto_save=False)

    assert first is True
    assert second is False
