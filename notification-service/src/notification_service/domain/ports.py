from typing import Protocol
from pydantic import BaseModel, EmailStr

class EmailCommand(BaseModel):
    target_email: EmailStr
    subject: str
    body: str
    reply_to: EmailStr

class EmailSenderPort(Protocol):
    async def send_email(self, command: EmailCommand) -> None:
        ...
