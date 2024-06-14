from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region_name: str
    sqs_queue_url: str
    port: int = Field(default=8000, env='APP_PORT')
    host: str = Field(default="0.0.0.0", env='APP_HOST')
    trainer_node_service_url: str = Field(..., env='TRAINER_NODE_SERVICE_URL')
    jwt_token: str = Field(..., env='JWT_TOKEN')

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
