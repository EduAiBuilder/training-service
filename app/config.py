# app/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region_name: str
    sqs_queue_url: str

    class Config:
        env_file = ".env"

settings = Settings()
