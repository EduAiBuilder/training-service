import time
from app.utils.sqs_handler import receive_messages, process_message

async def consume_sqs_messages():
    while True:
        messages = receive_messages()
        for message in messages:
            await process_message(message)
        time.sleep(5)
