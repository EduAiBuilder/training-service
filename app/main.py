from fastapi import FastAPI
import asyncio
from app.routes.health import router as health_router
from app.sqs_consumer import consume_sqs_messages
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the consume_sqs_messages task when the application starts
    task = asyncio.create_task(consume_sqs_messages())
    try:
        yield
    finally:
        # Cancel the task when the application shuts down
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("SQS consumer task was cancelled")

app.router.lifespan_context = lifespan

app.include_router(health_router, prefix="/health")