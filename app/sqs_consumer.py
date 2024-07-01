import asyncio
from app.utils.sqs_handler import receive_messages, process_message

async def consume_sqs_messages():
    while True:
        try:
            messages = receive_messages()
            for message in messages:
                await process_message(message)
            await asyncio.sleep(5)  # Use asyncio.sleep for non-blocking delay
        except Exception as e:
            print(f"Error in SQS consumer: {e}")
            await asyncio.sleep(5)  # Sleep before retrying on error