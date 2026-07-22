from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from router_service.domain.routing import RoutingTarget, AgentResponse
from router_service.domain.ports import NotificationPort, EmailCommand
from router_service.config import settings
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class RouterDependencies:
    notification_adapter: NotificationPort
    user_email: str

system_prompt = """
You are an intelligent message router. Your job is to analyze incoming messages from users
and route them to the appropriate department.

Available departments:
- human-resources@example.com (for HR related queries)
- help-desk@example.com (for general help or customer service)
- it@example.com (for technical issues, broken equipment, IT support)
- kadry@example.com (Polish equivalent of HR, matters related to payroll, holidays)
- other@example.com (fallback for anything else, or if you are unsure)

You must ALWAYS use the `send_email_tool` to dispatch the message to the chosen department.
For the target_email, use exactly one of the allowed routing targets.
For the reply_to, use the user's email address provided in your context.
For the subject, generate a brief and descriptive subject based on the message.
For the body, you can pass the original message or a slightly formatted version of it.
"""

ollama_model = OllamaModel(
    model_name=settings.llm_model,
    base_url=settings.ollama_base_url
)

router_agent = Agent[RouterDependencies, AgentResponse](
    model=ollama_model,
    system_prompt=system_prompt,
    result_type=AgentResponse,
)

@router_agent.tool
async def send_email_tool(ctx: RunContext[RouterDependencies], target_email: RoutingTarget, subject: str, body: str) -> str:
    """Sends an email to the selected department with the user's message."""
    command = EmailCommand(
        target_email=target_email.value,
        subject=subject,
        body=body,
        reply_to=ctx.deps.user_email
    )
    success = await ctx.deps.notification_adapter.send_email(command)
    if success:
        return f"Email successfully sent to {target_email.value}"
    else:
        return f"Failed to send email to {target_email.value}"
