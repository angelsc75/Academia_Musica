from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = "123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str

    class Config: str ="mysql+mysqlconnector://root:Luis.123@localhost:3306/escuela_musica"
    class Config:
        env_file = ".env"
settings = Settings()