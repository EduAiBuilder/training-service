# app/config.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region_name: str
    sqs_queue_url: str
    port: int = Field(default=8000, env='APP_PORT')

    class Config:
        env_file = ".env"

settings = Settings()
