import os
import pathlib

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, validator
from typing import List, Optional, Union


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent

dotenv_path = ROOT / '.env.local'
load_dotenv(dotenv_path)

class DBSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL')

class SummarizerSettings(BaseSettings):
    LANGUAGE: str = os.environ.get('LSA_SUMMARIZER_LANGUAGE')
    SENTENCES_COUNT: str = os.environ.get('LSA_SUMMARIZER_SENTENCES_COUNT')


class CelerySettings(BaseSettings):
    brocker: str = os.environ.get('CELERY_BROCKER_REDIS_URL')
    backend: str = os.environ.get('CELERY_BACKEND_REDIS_URL')


class RedisSettings(BaseSettings):
    url: str = os.environ.get('REDIS_CACHE_URL')
    summary_fail_key: str = os.environ.get('REDIS_SUMMARY_FAIL_KEY')


class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.environ.get('BACKEND_CORS_ORIGINS', [])

    # Origins that match this regex OR are in the above list are allowed
    BACKEND_CORS_ORIGIN_REGEX: Optional[str] = r'https://.*\.herokuapp.com'

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    db: DBSettings = DBSettings()
    lsa: SummarizerSettings = SummarizerSettings()
    celery: CelerySettings = CelerySettings()
    redis: RedisSettings = RedisSettings()

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
