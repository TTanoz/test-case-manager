import json
from pathlib import Path
import storage

def test_save_and_load_roundtrip(tmp_path):
    # Redirect DATA_PATH to a temp file
    storage.DATA_PATH = tmp_path / "data.json"

    data = storage.DEFAULT_DATA.copy()
    data["suites"].append({"id": 1, "name": "Login", "description": "Auth", "cases": []})
    storage.save_to_file(data)

    # Ensure file created
    assert storage.DATA_PATH.exists()
    raw = json.loads(storage.DATA_PATH.read_text(encoding="utf-8"))
    assert raw["suites"][0]["name"] == "Login"

    # Load
    loaded = storage.load_from_file()
    assert loaded["suites"][0]["description"] == "Auth"