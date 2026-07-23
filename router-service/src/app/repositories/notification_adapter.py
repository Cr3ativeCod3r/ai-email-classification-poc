import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
from app.models.ports import NotificationPort, EmailCommand
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class HTTPNotificationAdapter(NotificationPort):
    def __init__(self, base_url: str = settings.notification_service_url):
        self.base_url = base_url

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type(httpx.HTTPError),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )
    async def _send_with_retry(self, command: EmailCommand) -> bool:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                self.base_url,
                json=command.model_dump()
            )
            response.raise_for_status()
            return True

    async def send_email(self, command: EmailCommand) -> bool:
        try:
            return await self._send_with_retry(command)
        except httpx.HTTPError as e:
            logger.error(f"Failed to send email via notification service: {e}")
            return False
