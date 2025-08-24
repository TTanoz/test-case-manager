import json
from pathlib import Path
import copy

DATA_PATH = Path("data.json")

class DefaultData(dict):
    def copy(self):
        return copy.deepcopy(dict(self))


DEFAULT_DATA = DefaultData({
    "suites": [],
    "cases": [],
    "runs": [],
    "idx": 1,            # suite id counter
    "next_run_id": 9001  # run id counter
})

def save_to_file(data):
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")

def load_from_file():
    if not DATA_PATH.exists():
        return DEFAULT_DATA.copy()
    try:
        text = DATA_PATH.read_text(encoding="utf-8").strip()
        if not text:
            return DEFAULT_DATA.copy()
        data = json.loads(text)
        if not isinstance(data, dict):
            return DEFAULT_DATA.copy()
        data.setdefault("suites", [])
        data.setdefault("cases", [])
        data.setdefault("runs", [])
        data.setdefault("idx", 1)
        data.setdefault("next_run_id", 9001)
        return data
    except (json.JSONDecodeError, OSError):
        return DEFAULT_DATA.copy()