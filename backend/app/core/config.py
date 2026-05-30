from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    ENVIRONMENT: str = "development"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_SENSOR_TOPIC: str = "sensor-readings"

    # Satellite
    SENTINEL_HUB_CLIENT_ID: str = ""
    SENTINEL_HUB_CLIENT_SECRET: str = ""

    # ML
    MODEL_PATH: str = "ml/model/weights/soil_transformer.pt"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
