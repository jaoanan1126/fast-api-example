# Validates the type of env variables and that env var exists
from pydantic_settings import BaseSettings ,SettingsConfigDict
import os 
class Settings(BaseSettings):
    database_password: str 
    database_hostname: str
    database_port: str 
    database_name: str 
    database_username: str
    secret_key: str
    algorithm: str
    access_token_minutes: int

    class Config:
        env_file = ".env"
        
settings = Settings()
