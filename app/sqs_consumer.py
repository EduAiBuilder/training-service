import time
from app.utils.sqs_handler import receive_messages, process_message

def consume_sqs_messages():
    while True:
        messages = receive_messages()
        for message in messages:
            process_message(message)
        time.sleep(30)
