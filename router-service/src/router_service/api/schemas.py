from pydantic import BaseModel, EmailStr

class MessageRequest(BaseModel):
    email: EmailStr
    message: str

class MessageResponse(BaseModel):
    routed_to: str
    reasoning_summary: str
    status: str
