from enum import Enum
from pydantic import BaseModel, Field

class RoutingTarget(str, Enum):
    HUMAN_RESOURCES = "human-resources@example.com"
    HELP_DESK = "help-desk@example.com"
    IT = "it@example.com"
    KADRY = "kadry@example.com"
    OTHER = "other@example.com"

class AgentResponse(BaseModel):
    target: RoutingTarget = Field(description="The chosen department to route the message to.")
    reasoning: str = Field(description="Short summary explaining why this department was chosen.")
