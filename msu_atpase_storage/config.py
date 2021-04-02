from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    tg_token: str = Field(..., env="TG_TOKEN")
    aws_access_key_id: str = Field(..., env="AWSAccessKeyId")
    aws_secret_key: str = Field(..., env="AWSSecretKey")
    aws_busket: str = Field(..., env="AWSBusket")
    id_size: int = Field(..., env="ID_Size")
    mongo_host: str = Field("localhost", env="MONGO_HOST")
    mongo_port: str = Field(27017, env="MONGO_PORT")
    mongo_password: Optional[str] = Field(None, env="MONGO_PASSWORD")
    mongo_db_name: str = Field("aiogram_fsm", env="MONGO_DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
