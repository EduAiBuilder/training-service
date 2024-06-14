import boto3
from app.config import settings
import json
import httpx

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
    try:
        # Assuming the message body is JSON and contains a 'trainerId'
        body = json.loads(message['Body'])
        trainer_id = body.get('trainerId')
        if trainer_id:
            fetch_trainer_data(trainer_id)
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

def fetch_trainer_data(trainer_id):
    try:
        trainer_service_url = f"{settings.trainer_node_service_url}/trainers/{trainer_id}/images"
        headers = {
            "Authorization": f"Bearer {settings.jwt_token}"
        }
        response = httpx.get(trainer_service_url, headers=headers)
        response.raise_for_status()
        trainer_data = response.json()
        print(f"Fetched trainer data: {trainer_data}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error while fetching trainer data: {e}")
    except Exception as e:
        print(f"Error fetching trainer data: {e}")
