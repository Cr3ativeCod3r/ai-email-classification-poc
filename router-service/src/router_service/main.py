from fastapi import FastAPI
from router_service.api.routers import router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Router Service API",
    description="Intelligent message router using LLM",
    version="1.0.0",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json"
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
