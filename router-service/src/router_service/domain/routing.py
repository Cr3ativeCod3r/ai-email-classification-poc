import json
from pathlib import Path
from pydantic import BaseModel, Field

import os

# Go up 5 levels: domain -> router_service -> src -> router-service -> root
DEFAULT_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "departments.json"
DEPARTMENTS_FILE = Path(os.environ.get("DEPARTMENTS_FILE", DEFAULT_PATH))

with open(DEPARTMENTS_FILE, "r", encoding="utf-8") as f:
    DEPARTMENTS_DATA = json.load(f)

def get_fallback_email() -> str:
    for d in DEPARTMENTS_DATA:
        if d["shortcut"] == "OTHER":
            return d["email"]
    return "other@example.com"

class AgentResponse(BaseModel):
    target: str = Field(
        description="The target department email to route the message to.",
        json_schema_extra={"enum": [d["email"] for d in DEPARTMENTS_DATA]}
    )
    reasoning: str = Field(description="A brief explanation of why this department was selected.")
