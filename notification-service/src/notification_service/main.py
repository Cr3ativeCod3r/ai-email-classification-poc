from fastapi import FastAPI
from notification_service.api.routers import router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Notification Service API",
    description="Internal service for sending emails",
    version="1.0.0"
)

app.include_router(router, prefix="/internal/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
