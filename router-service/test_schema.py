import json
from pydantic import BaseModel, Field

DEPARTMENTS_DATA = [{"email": "hr@example.com"}]

class AgentResponse(BaseModel):
    target: str = Field(json_schema_extra={"enum": [d["email"] for d in DEPARTMENTS_DATA]})

print(AgentResponse.model_json_schema())
