from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    tg_token: str = Field(..., env="TG_TOKEN")
    aws_access_key_id: str = Field(..., env="AWSAccessKeyId")
    aws_secret_key: str = Field(..., env="AWSSecretKey")
    aws_busket: str = Field(..., env="AWSBusket")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
