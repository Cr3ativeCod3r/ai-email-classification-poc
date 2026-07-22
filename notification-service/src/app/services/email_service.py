from app.models.ports import EmailCommand
from app.repositories.smtp_adapter import SMTPEmailAdapter
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, email_adapter: SMTPEmailAdapter):
        self.email_adapter = email_adapter

    async def send_email(self, command: EmailCommand) -> None:
        logger.info(f"Processing email sending for {command.target_email}")
        await self.email_adapter.send_email(command)
