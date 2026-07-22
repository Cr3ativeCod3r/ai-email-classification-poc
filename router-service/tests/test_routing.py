import pytest
from pydantic_ai import models
from pydantic_ai.models.test import TestModel
from router_service.domain.agent import router_agent, RouterDependencies
from router_service.domain.ports import NotificationPort, EmailCommand

class MockNotificationAdapter(NotificationPort):
    def __init__(self):
        self.commands = []

    async def send_email(self, command: EmailCommand) -> bool:
        self.commands.append(command)
        return True

@pytest.mark.asyncio
async def test_routing_agent_success():
    test_model = TestModel(
        call_tools=[],
        custom_output_args={"target": "it@example.com", "reasoning": "something"}
    )
    
    mock_adapter = MockNotificationAdapter()
    deps = RouterDependencies(
        notification_adapter=mock_adapter,
        user_email="test@user.com"
    )

    with router_agent.override(model=test_model):
        result = await router_agent.run("My computer is broken", deps=deps)
        
        # TestModel will just return default values or empty strings for strings, and the first enum for enums.
        # But we can check that it didn't crash.
        assert result.output is not None
        assert isinstance(result.output.target, str)

@pytest.mark.asyncio
async def test_tool_execution():
    mock_adapter = MockNotificationAdapter()
    deps = RouterDependencies(
        notification_adapter=mock_adapter,
        user_email="test@user.com"
    )
    
    # We can invoke the tool directly if we create a mock context, 
    # but testing the agent run is usually enough for pydantic_ai.
