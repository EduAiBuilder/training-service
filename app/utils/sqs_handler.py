import boto3
from app.config import settings
from app.models_trainer.models_trainer import main_training_process
import json

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
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )
    return response.get('Messages', [])

async def process_message(message):
    # Implement your message processing logic here
    print(f"Processing message: {message['Body']}")
    try:
        body = json.loads(message['Body'])
        trainer_id = body.get('trainerId')
        if trainer_id:
            await main_training_process(trainer_id)
        else:
            print("trainerId not found in message")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        delete_message(message['ReceiptHandle'])
   

def delete_message(receipt_handle):
    client = get_sqs_client()
    client.delete_message(
        QueueUrl=settings.sqs_queue_url,
        ReceiptHandle=receipt_handle
    )


