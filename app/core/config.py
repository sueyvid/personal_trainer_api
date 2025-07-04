# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ✅ Adicione a DATABASE_URL aqui
    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = "sua_chave_secreta_super_segura_e_longa"
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
