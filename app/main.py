from fastapi import FastAPI
from app.routes.sqs_routes import router as sqs_router
from app.sqs_consumer import consume_sqs_messages
import threading
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup code: Start the SQS consumer in a separate thread
    thread = threading.Thread(target=consume_sqs_messages, daemon=True)
    thread.start()
    yield
    # Teardown code: Any cleanup code can be added here
    # For now, we're not stopping the thread explicitly since it's a daemon

# Attach the lifespan context manager
app.router.lifespan_context = lifespan

# Include the router for SQS-related routes
app.include_router(sqs_router, prefix="/sqs")
