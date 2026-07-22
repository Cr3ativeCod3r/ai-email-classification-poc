import aiosmtplib
from email.message import EmailMessage
from notification_service.domain.ports import EmailSenderPort, EmailCommand
from notification_service.config import settings
import logging

logger = logging.getLogger(__name__)

class SMTPEmailAdapter(EmailSenderPort):
    def __init__(self, host: str = settings.smtp_host, port: int = settings.smtp_port):
        self.host = host
        self.port = port

    async def send_email(self, command: EmailCommand) -> None:
        message = EmailMessage()
        message.set_content(command.body)
        message["Subject"] = command.subject
        message["From"] = "system@example.com"
        message["To"] = command.target_email
        message["Reply-To"] = command.reply_to

        try:
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
            )
            logger.info(f"Successfully sent email to {command.target_email}")
        except Exception as e:
            logger.error(f"Error sending email to {command.target_email}: {e}")
            raise
