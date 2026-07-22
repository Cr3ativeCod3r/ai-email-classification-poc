import pytest
from app.models.ports import EmailCommand
from app.repositories.smtp_adapter import SMTPEmailAdapter

class MockSMTPSender:
    def __init__(self):
        self.sent_messages = []

    async def send(self, message, hostname, port):
        self.sent_messages.append((message, hostname, port))

@pytest.mark.asyncio
async def test_smtp_email_adapter(monkeypatch):
    mock_sender = MockSMTPSender()
    
    # Mock aiosmtplib.send
    import aiosmtplib
    monkeypatch.setattr(aiosmtplib, "send", mock_sender.send)
    
    adapter = SMTPEmailAdapter(host="fake_host", port=1025)
    
    command = EmailCommand(
        target_email="test@target.com",
        subject="Test subject",
        body="Test body",
        reply_to="user@example.com"
    )
    
    await adapter.send_email(command)
    
    assert len(mock_sender.sent_messages) == 1
    msg, host, port = mock_sender.sent_messages[0]
    assert host == "fake_host"
    assert port == 1025
    assert msg["To"] == "test@target.com"
    assert msg["Reply-To"] == "user@example.com"
    assert msg["Subject"] == "Test subject"
