from typing import Protocol
from pydantic import BaseModel, EmailStr

class EmailCommand(BaseModel):
    target_email: EmailStr
    subject: str
    body: str
    reply_to: EmailStr

class NotificationPort(Protocol):
    async def send_email(self, command: EmailCommand) -> bool:
        ...

class RoutingResult(BaseModel):
    routed_to: str
    reasoning_summary: str

class RoutingAgentPort(Protocol):
    async def route_message(self, user_email: str, message: str) -> RoutingResult:
        ...
