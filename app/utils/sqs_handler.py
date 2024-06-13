import boto3
from app.config import settings

def get_sqs_client():
    return boto3.client(
        'sqs',
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region_name
    )

def receive_messages():
    client = get_sqs_client()
    response = client.receive_message(
        QueueUrl=settings.sqs_queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10
    )
    return response.get('Messages', [])

def process_message(message):
    # Implement your message processing logic here
    print(f"Processing message: {message['Body']}")
    # Delete the message after processing
    delete_message(message['ReceiptHandle'])

def delete_message(receipt_handle):
    client = get_sqs_client()
    client.delete_message(
        QueueUrl=settings.sqs_queue_url,
        ReceiptHandle=receipt_handle
    )
