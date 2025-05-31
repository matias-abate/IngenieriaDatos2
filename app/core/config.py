# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "mini_social"

    class Config:
        env_file = ".env"      
        env_file_encoding = "utf-8"

# instancia global
settings = Settings()
