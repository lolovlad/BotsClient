from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str
    host_server: str
    port_server: int


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')