from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from app.models.schemas import AgentResponse
from app.repositories.department_repository import DEPARTMENTS_DATA
from app.models.ports import NotificationPort, EmailCommand
from app.config import settings
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class RouterDependencies:
    notification_adapter: NotificationPort
    user_email: str
    email_sent_to: str | None = None

departments_list_str = "\n".join(
    f"- {d['email']} ({d['description']})" for d in DEPARTMENTS_DATA
)

system_prompt = f"""
You are an intelligent message router. Your job is to analyze incoming messages from users
and route them to the appropriate department.

Available departments:
{departments_list_str}

You must ALWAYS use the `send_email_tool` to dispatch the message to the chosen department.
For the target_email, use exactly one of the allowed routing targets.
For the reply_to, use the user's email address provided in your context.
For the subject, generate a brief and descriptive subject based on the message.
For the body, you can pass the original message or a slightly formatted version of it.
After successfully using the tool, you MUST return the final AgentResponse. Do not call the tool multiple times.
"""

ollama_url = settings.ollama_base_url
if not ollama_url.endswith("/v1"):
    ollama_url = f"{ollama_url.rstrip('/')}/v1"

try:
    from pydantic_ai.providers.openai import OpenAIProvider
    provider = OpenAIProvider(base_url=ollama_url, api_key="ollama")
    ollama_model = OllamaModel(
        model_name=settings.llm_model,
        provider=provider
    )
except ImportError:
    ollama_model = OllamaModel(model_name=settings.llm_model)

router_agent = Agent[RouterDependencies, AgentResponse](
    model=ollama_model,
    system_prompt=system_prompt,
    deps_type=RouterDependencies,
    output_type=AgentResponse,
)

@router_agent.tool
async def send_email_tool(ctx: RunContext[RouterDependencies], target_email: str, subject: str, body: str) -> str:
    """Sends an email to the selected department with the user's message."""
    if ctx.deps.email_sent_to is not None:
        return f"Email was already sent to {ctx.deps.email_sent_to}. Do not call this tool again. Please yield the final AgentResponse."

    command = EmailCommand(
        target_email=target_email,
        subject=subject,
        body=body,
        reply_to=ctx.deps.user_email
    )
    success = await ctx.deps.notification_adapter.send_email(command)
    if success:
        ctx.deps.email_sent_to = target_email
        return f"Email successfully sent to {target_email}. Please yield the final AgentResponse."
    else:
        return f"Failed to send email to {target_email}."
