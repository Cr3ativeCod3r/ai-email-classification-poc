from pydantic import BaseModel, EmailStr, Field
from app.repositories.department_repository import DEPARTMENTS_DATA
class MessageRequest(BaseModel):
    email: EmailStr
    message: str

class MessageResponse(BaseModel):
    routed_to: str
    reasoning_summary: str
    status: str

class AgentResponse(BaseModel):
    target: str = Field(
        description="The target department email to route the message to.",
        json_schema_extra={"enum": [d["email"] for d in DEPARTMENTS_DATA]}
    )
    reasoning: str = Field(description="A brief explanation of why this department was selected.")
