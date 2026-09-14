# BaseSettings: base class whose fields are populated from environment variables (or a .env file)
from pydantic_settings import BaseSettings, SettingsConfigDict


# Settings: every value the app needs that shouldn't be hardcoded in source (credentials, secrets)
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # env_file: tells pydantic-settings to read values from a ".env" file in the project root
    model_config = SettingsConfigDict(env_file=".env")


# settings: a single loaded instance, imported wherever a config value is needed
settings = Settings()
