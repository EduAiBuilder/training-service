import time
from app.utils.sqs_handler.py import receive_messages, process_message

def consume_sqs_messages():
    while True:
        messages = receive_messages()
        for message in messages:
            process_message(message)
        time.sleep(5)  # Adjust the interval as needed
