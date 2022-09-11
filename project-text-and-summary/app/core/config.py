import pathlib

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class DBSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///example.db"


class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8001"
    ]

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

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
