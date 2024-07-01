import boto3
import os
from app.config import settings


def upload_to_s3(trainer_id:int, export_path: str, model_key: str):
    s3_client = boto3.client('s3',
                             aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region_name
                             )
    s3_object_key = f'models/{trainer_id}/{model_key}.pkl'

    bucket = 'edu-ai-builder'
    try:
        # Open the file at export_path in binary read mode
        with open(export_path, 'rb') as file_obj:
            # Upload the file to S3 using the file object
            s3_client.upload_fileobj(file_obj, bucket, s3_object_key)
        
        print(f'Model successfully uploaded to s3://{bucket}/{s3_object_key}')

        os.remove(export_path)
        print(f'Local file {export_path} has been removed successfully.')
    except Exception as e:
        print(f'Error uploading model to S3: {e}')
    return s3_object_key