from fastapi import APIRouter, Depends, HTTPException
from notification_service.domain.ports import EmailCommand
from notification_service.infrastructure.smtp_adapter import SMTPEmailAdapter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_email_adapter() -> SMTPEmailAdapter:
    return SMTPEmailAdapter()

@router.post("/emails")
async def send_email(
    command: EmailCommand,
    email_adapter: SMTPEmailAdapter = Depends(get_email_adapter)
):
    try:
        await email_adapter.send_email(command)
        return {"status": "sent"}
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")
