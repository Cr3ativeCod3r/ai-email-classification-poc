import json
from pathlib import Path

import os

_docker_path = Path(__file__).resolve().parent.parent.parent.parent / "departments.json"
_local_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "departments.json"

if _docker_path.exists():
    DEFAULT_PATH = _docker_path
else:
    DEFAULT_PATH = _local_path

DEPARTMENTS_FILE = Path(os.environ.get("DEPARTMENTS_FILE", DEFAULT_PATH))

with open(DEPARTMENTS_FILE, "r", encoding="utf-8") as f:
    DEPARTMENTS_DATA = json.load(f)

def get_fallback_email() -> str:
    for d in DEPARTMENTS_DATA:
        if d["shortcut"] == "OTHER":
            return d["email"]
    return "other@example.com"

