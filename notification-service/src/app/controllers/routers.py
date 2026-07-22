from fastapi import APIRouter, Depends, HTTPException
from app.models.ports import EmailCommand
from app.repositories.smtp_adapter import SMTPEmailAdapter
from app.services.email_service import EmailService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_email_adapter() -> SMTPEmailAdapter:
    return SMTPEmailAdapter()

def get_email_service(
    email_adapter: SMTPEmailAdapter = Depends(get_email_adapter)
) -> EmailService:
    return EmailService(email_adapter)

@router.post("/emails")
async def send_email(
    command: EmailCommand,
    email_service: EmailService = Depends(get_email_service)
):
    try:
        await email_service.send_email(command)
        return {"status": "sent"}
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")
