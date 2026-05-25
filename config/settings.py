"""
Genes Platform Configuration
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Application
    app_name: str = "Genes Agent Factory"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    
    # Database
    database_url: str = "postgresql+asyncpg://genes:genes_password@localhost:5432/genes"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Docker
    docker_socket: str = "unix:///var/run/docker.sock"
    docker_network: str = "genes_network"
    
    # Security
    secret_key: str = "CHANGE_THIS_IN_PRODUCTION"
    api_key_header: str = "X-API-Key"
    
    # Agent Settings
    max_agents: int = 50
    agent_approval_required: bool = True
    agent_container_prefix: str = "genes_agent_"
    agent_base_image: str = "python:3.11-slim"
    
    # Monitoring
    enable_metrics: bool = True
    log_level: str = "INFO"
    
    # Paths
    templates_dir: str = "/app/agente_constructor/templates"
    agents_dir: str = "/app/agents/generated"


settings = Settings()
