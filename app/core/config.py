from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    mongo_uri: str = Field(default="mongodb://localhost:27017", env="MONGO_URI")
    mongo_db:   str = Field(default="mini_social",             env="MONGO_DB")

    neo4j_uri:      str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    neo4j_user:     str = Field(default="neo4j",                env="NEO4J_USER")
    neo4j_password: str = Field(default="secret",               env="NEO4J_PASSWORD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
