from fastapi import APIRouter, Depends, HTTPException
from router_service.api.schemas import MessageRequest, MessageResponse
from router_service.domain.agent import router_agent, RouterDependencies
from router_service.infrastructure.notification_adapter import HTTPNotificationAdapter
from pydantic_ai.exceptions import UnexpectedModelBehavior
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_notification_adapter() -> HTTPNotificationAdapter:
    return HTTPNotificationAdapter()

@router.post("/messages", response_model=MessageResponse)
async def process_message(
    request: MessageRequest,
    notification_adapter: HTTPNotificationAdapter = Depends(get_notification_adapter)
):
    deps = RouterDependencies(
        notification_adapter=notification_adapter,
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
        # Fallback handling in case LLM fails or doesn't follow schema perfectly
        from router_service.domain.routing import get_fallback_email
        from router_service.domain.ports import EmailCommand
        
        fallback_target = get_fallback_email()
        command = EmailCommand(
            target_email=fallback_target,
            subject="Fallback Subject",
            body=request.message,
            reply_to=request.email
        )
        await notification_adapter.send_email(command)
        
        return MessageResponse(
            routed_to=fallback_target,
            reasoning_summary="Fallback due to LLM error.",
            status="sent"
        )
