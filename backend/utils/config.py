from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration from .env"""
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_auth_logs_topic: str = "auth_logs"
    
    # Elasticsearch
    es_host: str = "localhost"
    es_port: int = 9200
    es_index_name: str = "security-logs"
    
    # ML
    ml_model_path: str = "./ml_models/isolation_forest.pkl"
    ml_contamination: float = 0.1
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
