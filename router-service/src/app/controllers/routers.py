from fastapi import APIRouter, Depends
from app.models.schemas import MessageRequest, MessageResponse
from app.repositories.notification_adapter import HTTPNotificationAdapter
from app.services.message_service import MessageService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_notification_adapter() -> HTTPNotificationAdapter:
    return HTTPNotificationAdapter()

def get_message_service(
    notification_adapter: HTTPNotificationAdapter = Depends(get_notification_adapter)
) -> MessageService:
    return MessageService(notification_adapter)

@router.post("/messages", response_model=MessageResponse)
async def process_message(
    request: MessageRequest,
    message_service: MessageService = Depends(get_message_service)
):
    return await message_service.process_message(request)
