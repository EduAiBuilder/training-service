from fastapi import FastAPI
from app.routes.health import router as health_router
from app.sqs_consumer import consume_sqs_messages
import threading
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=consume_sqs_messages, daemon=True)
    thread.start()
    yield

app.router.lifespan_context = lifespan

app.include_router(health_router, prefix="/health")
