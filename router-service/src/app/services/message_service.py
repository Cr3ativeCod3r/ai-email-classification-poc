from app.models.schemas import MessageRequest, MessageResponse
from app.services.agent import router_agent, RouterDependencies
from app.repositories.notification_adapter import HTTPNotificationAdapter
from app.repositories.department_repository import get_fallback_email
from app.models.ports import EmailCommand
import logging

logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self, notification_adapter: HTTPNotificationAdapter):
        self.notification_adapter = notification_adapter

    async def process_message(self, request: MessageRequest) -> MessageResponse:
        deps = RouterDependencies(
            notification_adapter=self.notification_adapter,
            user_email=request.email
        )
        
        try:
            result = await router_agent.run(request.message, deps=deps)
            return MessageResponse(
                routed_to=result.output.target,
                reasoning_summary=result.output.reasoning,
                status="sent"
            )
        except Exception as e:
            logger.error(f"Agent failed to process message: {e}")
            fallback_target = get_fallback_email()
            command = EmailCommand(
                target_email=fallback_target,
                subject="Fallback Subject",
                body=request.message,
                reply_to=request.email
            )
            await self.notification_adapter.send_email(command)
            
            return MessageResponse(
                routed_to=fallback_target,
                reasoning_summary="Fallback due to LLM error.",
                status="sent"
            )
