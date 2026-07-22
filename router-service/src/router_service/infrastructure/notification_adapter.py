import httpx
from router_service.domain.ports import NotificationPort, EmailCommand
from router_service.config import settings
import logging

logger = logging.getLogger(__name__)

class HTTPNotificationAdapter(NotificationPort):
    def __init__(self, base_url: str = settings.notification_service_url):
        self.base_url = base_url

    async def send_email(self, command: EmailCommand) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    json=command.model_dump()
                )
                response.raise_for_status()
                return True
        except httpx.HTTPError as e:
            logger.error(f"Failed to send email via notification service: {e}")
            return False
