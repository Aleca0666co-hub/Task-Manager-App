import os
from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    VERSION: str
    DATABASE_URL: str
    LOG_DIR: str
    LOG_FILE: str
    LOG_LEVEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        populate_by_name=True)

settings = Settings()


#   print(settings.APP_NAME)
#  env_file=os.path.join("../",".env")